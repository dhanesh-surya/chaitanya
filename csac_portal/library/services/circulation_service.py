from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from library.models import (
    BookCopy, LibraryRequest, CirculationTransaction, Fine,
    LibrarySetting, AuditLog, StudentProfile
)


def log_audit(user, action, reference_id, description, ip_address=None):
    AuditLog.objects.create(
        user=user,
        action=action,
        reference_id=str(reference_id),
        description=description,
        ip_address=ip_address
    )


def calculate_overdue_fine(transaction_obj, settings=None):
    if not settings:
        settings = LibrarySetting.get_settings()

    if transaction_obj.status in ['ISSUED', 'RETURN_REQUESTED']:
        today = timezone.now().date()
        if today > transaction_obj.due_date:
            days = (today - transaction_obj.due_date).days
            return days * settings.fine_per_day, days
    return 0.00, 0


@transaction.atomic
def create_book_request(student_profile, book_copy_id, remark="", ip_address=None):
    settings = LibrarySetting.get_settings()

    # Rule BR-05: Account Eligibility
    if not student_profile.is_library_eligible or student_profile.status != 'ACTIVE':
        raise ValidationError("Your library borrowing privileges are currently not active. Please contact the library desk.")

    # Rule BR-04: Overdue Suspension
    if student_profile.has_overdue and not settings.allow_borrowing_if_fines:
        raise ValidationError("You have an overdue book. Please return all overdue books before requesting new ones.")

    # Rule BR-03: Max Borrowing Quota
    current_issued = student_profile.active_issued_count
    if current_issued >= settings.max_books_per_student:
        raise ValidationError(f"Borrowing limit reached. You currently have {current_issued} issued books (maximum allowed is {settings.max_books_per_student}).")

    # Rule BR-02: Active Request Limit
    pending_count = student_profile.pending_requests_count
    if pending_count >= settings.max_pending_requests:
        raise ValidationError(f"You already have {pending_count} active pending/approved requests. Maximum allowed is {settings.max_pending_requests}.")

    # Lock copy row
    try:
        copy = BookCopy.objects.select_for_update().get(id=book_copy_id, is_active=True)
    except BookCopy.DoesNotExist:
        raise ValidationError("The requested book copy does not exist or has been deactivated.")

    # Rule BR-06: Copy availability
    if copy.status != 'AVAILABLE':
        raise ValidationError(f"This copy ({copy.accession_number}) is currently {copy.get_status_display().lower()} and cannot be requested.")

    # Rule BR-07: Duplicate request check
    active_requests = LibraryRequest.objects.filter(
        student=student_profile,
        book_copy__book=copy.book,
        status__in=['PENDING', 'APPROVED']
    ).exists()
    if active_requests:
        raise ValidationError("You already have an active request for a copy of this book.")

    has_issued_copy = CirculationTransaction.objects.filter(
        student=student_profile,
        book_copy__book=copy.book,
        status__in=['ISSUED', 'RETURN_REQUESTED']
    ).exists()
    if has_issued_copy:
        raise ValidationError("You currently have a copy of this book already issued to your account.")

    # Create Request
    req = LibraryRequest.objects.create(
        student=student_profile,
        book_copy=copy,
        student_remark=remark,
        status='PENDING'
    )

    copy.status = 'REQUESTED'
    copy.save(update_fields=['status', 'updated_at'])

    log_audit(
        user=student_profile.user,
        action='REQUEST_CREATED',
        reference_id=req.request_number,
        description=f"Student {student_profile.enrollment_number} requested copy {copy.accession_number} ({copy.book.title})",
        ip_address=ip_address
    )

    return req


@transaction.atomic
def cancel_book_request(student_profile, request_id, ip_address=None):
    try:
        req = LibraryRequest.objects.select_for_update().get(id=request_id, student=student_profile)
    except LibraryRequest.DoesNotExist:
        raise ValidationError("Request not found.")

    if req.status != 'PENDING':
        raise ValidationError(f"Cannot cancel request in '{req.get_status_display()}' status.")

    req.status = 'CANCELLED'
    req.save(update_fields=['status'])

    copy = req.book_copy
    if copy.status == 'REQUESTED':
        copy.status = 'AVAILABLE'
        copy.save(update_fields=['status', 'updated_at'])

    log_audit(
        user=student_profile.user,
        action='REQUEST_CANCELLED',
        reference_id=req.request_number,
        description=f"Student {student_profile.enrollment_number} cancelled request for {copy.accession_number}",
        ip_address=ip_address
    )

    return req


@transaction.atomic
def approve_book_request(librarian_user, request_id, expiry_days=None, ip_address=None):
    settings = LibrarySetting.get_settings()
    if not expiry_days:
        expiry_days = settings.request_expiry_days

    try:
        req = LibraryRequest.objects.select_for_update().get(id=request_id)
    except LibraryRequest.DoesNotExist:
        raise ValidationError("Request not found.")

    if req.status != 'PENDING':
        raise ValidationError(f"Request is not pending (currently: {req.get_status_display()}).")

    copy = req.book_copy
    req.status = 'APPROVED'
    req.reviewed_by = librarian_user
    req.reviewed_at = timezone.now()
    req.expiry_date = timezone.now() + timedelta(days=expiry_days)
    req.save()

    copy.status = 'RESERVED'
    copy.save(update_fields=['status', 'updated_at'])

    log_audit(
        user=librarian_user,
        action='REQUEST_APPROVED',
        reference_id=req.request_number,
        description=f"Approved request {req.request_number} for {copy.accession_number} by {librarian_user.username}",
        ip_address=ip_address
    )

    return req


@transaction.atomic
def reject_book_request(librarian_user, request_id, reason="Request rejected by library administration", ip_address=None):
    try:
        req = LibraryRequest.objects.select_for_update().get(id=request_id)
    except LibraryRequest.DoesNotExist:
        raise ValidationError("Request not found.")

    if req.status not in ['PENDING', 'APPROVED']:
        raise ValidationError(f"Cannot reject request in '{req.get_status_display()}' status.")

    copy = req.book_copy
    req.status = 'REJECTED'
    req.reviewed_by = librarian_user
    req.reviewed_at = timezone.now()
    req.rejection_reason = reason
    req.save()

    copy.status = 'AVAILABLE'
    copy.save(update_fields=['status', 'updated_at'])

    log_audit(
        user=librarian_user,
        action='REQUEST_REJECTED',
        reference_id=req.request_number,
        description=f"Rejected request {req.request_number} ({reason})",
        ip_address=ip_address
    )

    return req


@transaction.atomic
def issue_physical_book(librarian_user, request_id=None, student_profile=None, book_copy=None, condition='GOOD', loan_days=None, ip_address=None):
    settings = LibrarySetting.get_settings()
    if not loan_days:
        loan_days = settings.default_loan_days

    req = None
    if request_id:
        req = LibraryRequest.objects.select_for_update().get(id=request_id)
        if req.status != 'APPROVED':
            raise ValidationError(f"Request must be in 'APPROVED' status before physical handover (Current: {req.get_status_display()}).")
        student_profile = req.student
        book_copy = req.book_copy
    else:
        if not student_profile or not book_copy:
            raise ValidationError("Student profile and Book copy are required for direct issuance.")
        if book_copy.status != 'AVAILABLE':
            raise ValidationError(f"Copy {book_copy.accession_number} is {book_copy.get_status_display()} and cannot be issued.")

    # Validate quota at time of issue
    if student_profile.active_issued_count >= settings.max_books_per_student:
        raise ValidationError(f"Student has already reached the maximum book limit ({settings.max_books_per_student}).")

    due_date = timezone.now().date() + timedelta(days=loan_days)

    txn = CirculationTransaction.objects.create(
        request=req,
        student=student_profile,
        book_copy=book_copy,
        issued_by=librarian_user,
        issued_at=timezone.now(),
        due_date=due_date,
        status='ISSUED',
        condition_at_issue=condition
    )

    if req:
        req.status = 'ISSUED'
        req.save(update_fields=['status'])

    book_copy.status = 'ISSUED'
    book_copy.condition = condition
    book_copy.save(update_fields=['status', 'condition', 'updated_at'])

    log_audit(
        user=librarian_user,
        action='BOOK_ISSUED',
        reference_id=txn.transaction_number,
        description=f"Issued copy {book_copy.accession_number} to student {student_profile.enrollment_number} (Due: {due_date})",
        ip_address=ip_address
    )

    return txn


@transaction.atomic
def request_book_return(student_profile, transaction_id, remark="", ip_address=None):
    try:
        txn = CirculationTransaction.objects.select_for_update().get(
            id=transaction_id,
            student=student_profile
        )
    except CirculationTransaction.DoesNotExist:
        raise ValidationError("Transaction not found or does not belong to you.")

    if txn.status != 'ISSUED':
        raise ValidationError(f"Return cannot be initiated for transaction with status '{txn.get_status_display()}'.")

    txn.status = 'RETURN_REQUESTED'
    txn.return_requested_at = timezone.now()
    txn.return_request_remark = remark
    txn.save(update_fields=['status', 'return_requested_at', 'return_request_remark'])

    copy = txn.book_copy
    copy.status = 'RETURN_REQUESTED'
    copy.save(update_fields=['status', 'updated_at'])

    log_audit(
        user=student_profile.user,
        action='RETURN_REQUESTED',
        reference_id=txn.transaction_number,
        description=f"Student {student_profile.enrollment_number} initiated return for {copy.accession_number}",
        ip_address=ip_address
    )

    return txn


@transaction.atomic
def confirm_book_return(librarian_user, transaction_id, condition='GOOD', waive_fine=False, remarks="", ip_address=None):
    try:
        txn = CirculationTransaction.objects.select_for_update().get(id=transaction_id)
    except CirculationTransaction.DoesNotExist:
        raise ValidationError("Circulation transaction not found.")

    if txn.status not in ['ISSUED', 'RETURN_REQUESTED']:
        raise ValidationError(f"Book is already marked as '{txn.get_status_display()}'.")

    settings = LibrarySetting.get_settings()
    fine_amount, overdue_days = calculate_overdue_fine(txn, settings)

    txn.returned_at = timezone.now()
    txn.returned_by = librarian_user
    txn.status = 'RETURNED'
    txn.condition_at_return = condition
    txn.remarks = remarks

    if condition == 'DAMAGED':
        txn.status = 'DAMAGED'
    elif condition == 'LOST':
        txn.status = 'LOST'

    if overdue_days > 0 and not waive_fine:
        txn.fine_amount = fine_amount
        txn.fine_paid = False
        Fine.objects.create(
            transaction=txn,
            student=txn.student,
            amount=fine_amount,
            overdue_days=overdue_days,
            is_settled=False,
            remarks=f"Overdue by {overdue_days} days (Rate: ₹{settings.fine_per_day}/day)"
        )
    elif waive_fine:
        txn.remarks += " [Fine Waived by Librarian]"

    txn.save()

    copy = txn.book_copy
    if condition == 'DAMAGED':
        copy.status = 'DAMAGED'
    elif condition == 'LOST':
        copy.status = 'LOST'
    else:
        copy.status = 'AVAILABLE'
    copy.condition = condition
    copy.save(update_fields=['status', 'condition', 'updated_at'])

    log_audit(
        user=librarian_user,
        action='RETURN_CONFIRMED',
        reference_id=txn.transaction_number,
        description=f"Confirmed physical return of {copy.accession_number} from {txn.student.enrollment_number}. Fine: ₹{txn.fine_amount}",
        ip_address=ip_address
    )

    return txn
