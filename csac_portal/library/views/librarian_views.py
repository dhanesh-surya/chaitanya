from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q
from library.models import (
    LibraryRequest, CirculationTransaction, BookCopy, StudentProfile, Fine, LibrarySetting, AuditLog
)
from library.decorators import librarian_required
from library.services.circulation_service import (
    approve_book_request, reject_book_request, issue_physical_book, confirm_book_return, calculate_overdue_fine
)


def staff_login_view(request):
    if request.user.is_authenticated and (request.user.is_staff or hasattr(request.user, 'library_staff_profile')):
        return redirect('library:librarian_dashboard')

    if request.method == 'POST':
        identifier = request.POST.get('identifier', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=identifier, password=password)
        if user is not None and (user.is_staff or hasattr(user, 'library_staff_profile')):
            login(request, user)
            messages.success(request, f"Welcome to Librarian Circulation Desk, {user.get_full_name() or user.username}!")
            return redirect('library:librarian_dashboard')
        else:
            messages.error(request, "Invalid staff username or password, or insufficient permissions.")

    return render(request, 'library/librarian/login.html', {
        'page_title': 'Librarian Desk Login',
        'breadcrumb': 'Staff Portal'
    })


@librarian_required
def librarian_dashboard(request):
    today = timezone.now().date()

    pending_requests_count = LibraryRequest.objects.filter(status='PENDING').count()
    approved_requests_count = LibraryRequest.objects.filter(status='APPROVED').count()
    return_requests_count = CirculationTransaction.objects.filter(status='RETURN_REQUESTED').count()
    
    today_issues_count = CirculationTransaction.objects.filter(issued_at__date=today).count()
    today_returns_count = CirculationTransaction.objects.filter(returned_at__date=today).count()

    overdue_txns = CirculationTransaction.objects.filter(
        status__in=['ISSUED', 'RETURN_REQUESTED'],
        due_date__lt=today
    ).select_related('student__user', 'book_copy__book')
    overdue_count = overdue_txns.count()

    pending_registrations_count = StudentProfile.objects.filter(status='PENDING_APPROVAL').count()
    recent_requests = LibraryRequest.objects.filter(status='PENDING').select_related('student__user', 'book_copy__book').order_by('-requested_at')[:5]

    context = {
        'page_title': 'Librarian Operational Dashboard',
        'breadcrumb': 'Circulation Control',
        'pending_requests_count': pending_requests_count,
        'approved_requests_count': approved_requests_count,
        'return_requests_count': return_requests_count,
        'today_issues_count': today_issues_count,
        'today_returns_count': today_returns_count,
        'overdue_count': overdue_count,
        'pending_registrations_count': pending_registrations_count,
        'recent_requests': recent_requests,
    }
    return render(request, 'library/librarian/dashboard.html', context)


@librarian_required
def student_registrations_queue(request):
    status_filter = request.GET.get('status', 'PENDING_APPROVAL')
    search_q = request.GET.get('q', '').strip()

    profiles = StudentProfile.objects.select_related('user', 'department').order_by('-created_at')

    if status_filter != 'ALL':
        profiles = profiles.filter(status=status_filter)

    if search_q:
        profiles = profiles.filter(
            Q(enrollment_number__icontains=search_q) |
            Q(library_card_number__icontains=search_q) |
            Q(user__first_name__icontains=search_q) |
            Q(user__last_name__icontains=search_q) |
            Q(user__username__icontains=search_q) |
            Q(course__icontains=search_q) |
            Q(mobile__icontains=search_q)
        )

    pending_count = StudentProfile.objects.filter(status='PENDING_APPROVAL').count()

    context = {
        'page_title': 'Student Library Registrations',
        'breadcrumb': 'Membership Approvals',
        'profiles': profiles[:100],
        'status_filter': status_filter,
        'search_q': search_q,
        'pending_count': pending_count,
    }
    return render(request, 'library/librarian/student_registrations.html', context)


@librarian_required
def approve_student_registration(request, student_id):
    if request.method != 'POST':
        return redirect('library:librarian_registrations')

    student = get_object_or_404(StudentProfile, id=student_id)
    card_number = request.POST.get('library_card_number', '').strip() or student.library_card_number

    # Ensure card number uniqueness
    if StudentProfile.objects.exclude(id=student.id).filter(library_card_number__iexact=card_number).exists():
        messages.error(request, f"Library Card Number '{card_number}' is already assigned to another student.")
        return redirect('library:librarian_registrations')

    student.library_card_number = card_number
    student.status = 'ACTIVE'
    student.is_library_eligible = True
    student.approved_by = request.user
    student.approved_at = timezone.now()
    student.rejection_reason = ""
    student.save()

    AuditLog.objects.create(
        user=request.user,
        action='STUDENT_APPROVED',
        reference_id=student.enrollment_number,
        description=f"Librarian {request.user.username} approved library membership for student {student.full_name} ({student.enrollment_number}). Card No: {student.library_card_number}",
        ip_address=request.META.get('REMOTE_ADDR')
    )

    messages.success(request, f"Student {student.full_name} ({student.enrollment_number}) has been approved! They can now log in to the Student Library Portal.")
    return redirect('library:librarian_registrations')


@librarian_required
def reject_student_registration(request, student_id):
    if request.method != 'POST':
        return redirect('library:librarian_registrations')

    student = get_object_or_404(StudentProfile, id=student_id)
    reason = request.POST.get('rejection_reason', '').strip()

    student.status = 'REJECTED'
    student.is_library_eligible = False
    student.rejection_reason = reason
    student.save()

    AuditLog.objects.create(
        user=request.user,
        action='STUDENT_REJECTED',
        reference_id=student.enrollment_number,
        description=f"Librarian {request.user.username} rejected membership for student {student.full_name} ({student.enrollment_number}). Reason: {reason}",
        ip_address=request.META.get('REMOTE_ADDR')
    )

    messages.warning(request, f"Registration for student {student.full_name} ({student.enrollment_number}) was rejected.")
    return redirect('library:librarian_registrations')


@librarian_required
def requests_queue(request):
    status_filter = request.GET.get('status', 'PENDING')
    search_q = request.GET.get('q', '').strip()

    requests_qs = LibraryRequest.objects.select_related('student__user', 'book_copy__book').order_by('-requested_at')

    if status_filter != 'ALL':
        requests_qs = requests_qs.filter(status=status_filter)

    if search_q:
        requests_qs = requests_qs.filter(
            Q(request_number__icontains=search_q) |
            Q(student__enrollment_number__icontains=search_q) |
            Q(student__user__first_name__icontains=search_q) |
            Q(book_copy__accession_number__icontains=search_q) |
            Q(book_copy__book__title__icontains=search_q)
        )

    context = {
        'page_title': 'Book Request Queue',
        'breadcrumb': 'Requests Management',
        'requests_list': requests_qs,
        'status_filter': status_filter,
        'search_q': search_q,
    }
    return render(request, 'library/librarian/requests_queue.html', context)


@librarian_required
def approve_request_action(request, request_id):
    if request.method != 'POST':
        return redirect('library:librarian_requests')

    ip_addr = request.META.get('REMOTE_ADDR')
    try:
        req = approve_book_request(request.user, request_id, ip_address=ip_addr)
        messages.success(request, f"Request {req.request_number} approved! Copy {req.book_copy.accession_number} is now RESERVED for pickup.")
    except ValidationError as e:
        messages.error(request, str(e.message if hasattr(e, 'message') else e))
    except Exception as e:
        messages.error(request, f"Could not approve request: {str(e)}")

    return redirect('library:librarian_requests')


@librarian_required
def reject_request_action(request, request_id):
    if request.method != 'POST':
        return redirect('library:librarian_requests')

    reason = request.POST.get('reason', 'Rejected by library administration').strip()
    ip_addr = request.META.get('REMOTE_ADDR')
    try:
        req = reject_book_request(request.user, request_id, reason=reason, ip_address=ip_addr)
        messages.info(request, f"Request {req.request_number} rejected. Copy has been released back to shelf.")
    except ValidationError as e:
        messages.error(request, str(e.message if hasattr(e, 'message') else e))
    except Exception as e:
        messages.error(request, f"Could not reject request: {str(e)}")

    return redirect('library:librarian_requests')


@librarian_required
def issue_desk(request):
    query = request.GET.get('q', '').strip()
    target_request = None
    target_copy = None
    target_student = None

    if query:
        # Check if query is a request number
        target_request = LibraryRequest.objects.filter(request_number__iexact=query).select_related('student__user', 'book_copy__book').first()
        if not target_request:
            # Check if query is an accession number
            target_copy = BookCopy.objects.filter(accession_number__iexact=query, is_active=True).select_related('book').first()
        if not target_request and not target_copy:
            # Check if query is an enrollment number
            target_student = StudentProfile.objects.filter(enrollment_number__iexact=query).select_related('user').first()

    settings = LibrarySetting.get_settings()
    approved_requests = LibraryRequest.objects.filter(status='APPROVED').select_related('student__user', 'book_copy__book').order_by('expiry_date')[:10]

    context = {
        'page_title': 'Physical Book Issue Desk',
        'breadcrumb': 'Issue Counter',
        'query': query,
        'target_request': target_request,
        'target_copy': target_copy,
        'target_student': target_student,
        'approved_requests': approved_requests,
        'settings': settings,
    }
    return render(request, 'library/librarian/issue_desk.html', context)


@librarian_required
def confirm_issue_action(request):
    if request.method != 'POST':
        return redirect('library:librarian_issue')

    request_id = request.POST.get('request_id')
    accession_number = request.POST.get('accession_number', '').strip()
    enrollment_number = request.POST.get('enrollment_number', '').strip()
    condition = request.POST.get('condition', 'GOOD')
    ip_addr = request.META.get('REMOTE_ADDR')

    try:
        if request_id:
            txn = issue_physical_book(request.user, request_id=request_id, condition=condition, ip_address=ip_addr)
        else:
            copy = BookCopy.objects.get(accession_number__iexact=accession_number, is_active=True)
            student = StudentProfile.objects.get(enrollment_number__iexact=enrollment_number)
            txn = issue_physical_book(request.user, student_profile=student, book_copy=copy, condition=condition, ip_address=ip_addr)

        messages.success(request, f"Physical Book Issued Successfully! Transaction No: {txn.transaction_number}. Due Date: {txn.due_date.strftime('%d %b %Y')}.")
    except (BookCopy.DoesNotExist, StudentProfile.DoesNotExist):
        messages.error(request, "Invalid Accession Number or Student Enrollment Number.")
    except ValidationError as e:
        messages.error(request, str(e.message if hasattr(e, 'message') else e))
    except Exception as e:
        messages.error(request, f"Failed to issue book: {str(e)}")

    return redirect('library:librarian_issue')


@librarian_required
def return_desk(request):
    query = request.GET.get('q', '').strip()
    target_txn = None

    if query:
        target_txn = CirculationTransaction.objects.filter(
            status__in=['ISSUED', 'RETURN_REQUESTED']
        ).filter(
            Q(book_copy__accession_number__iexact=query) |
            Q(transaction_number__iexact=query)
        ).select_related('student__user', 'book_copy__book').first()

    return_queue = CirculationTransaction.objects.filter(
        status='RETURN_REQUESTED'
    ).select_related('student__user', 'book_copy__book').order_by('-return_requested_at')

    active_issues = CirculationTransaction.objects.filter(
        status='ISSUED'
    ).select_related('student__user', 'book_copy__book').order_by('due_date')[:15]

    settings = LibrarySetting.get_settings()
    calculated_fine = 0.00
    overdue_days = 0
    if target_txn:
        calculated_fine, overdue_days = calculate_overdue_fine(target_txn, settings)

    context = {
        'page_title': 'Book Return Desk',
        'breadcrumb': 'Return Counter',
        'query': query,
        'target_txn': target_txn,
        'return_queue': return_queue,
        'active_issues': active_issues,
        'calculated_fine': calculated_fine,
        'overdue_days': overdue_days,
        'settings': settings,
    }
    return render(request, 'library/librarian/return_desk.html', context)


@librarian_required
def confirm_return_action(request, transaction_id):
    if request.method != 'POST':
        return redirect('library:librarian_returns')

    condition = request.POST.get('condition', 'GOOD')
    waive_fine = request.POST.get('waive_fine') == 'on'
    remarks = request.POST.get('remarks', '').strip()
    ip_addr = request.META.get('REMOTE_ADDR')

    try:
        txn = confirm_book_return(
            request.user,
            transaction_id,
            condition=condition,
            waive_fine=waive_fine,
            remarks=remarks,
            ip_address=ip_addr
        )
        fine_msg = f" Overdue Fine: ₹{txn.fine_amount} recorded." if txn.fine_amount > 0 else ""
        messages.success(request, f"Book copy {txn.book_copy.accession_number} return confirmed! Copy is now {txn.book_copy.get_status_display()}.{fine_msg}")
    except ValidationError as e:
        messages.error(request, str(e.message if hasattr(e, 'message') else e))
    except Exception as e:
        messages.error(request, f"Failed to confirm return: {str(e)}")

    return redirect('library:librarian_returns')


@librarian_required
def overdue_monitor(request):
    today = timezone.now().date()
    overdue_records = CirculationTransaction.objects.filter(
        status__in=['ISSUED', 'RETURN_REQUESTED'],
        due_date__lt=today
    ).select_related('student__user', 'book_copy__book').order_by('due_date')

    settings = LibrarySetting.get_settings()
    enriched_records = []
    total_estimated_fine = 0

    for rec in overdue_records:
        fine, days = calculate_overdue_fine(rec, settings)
        total_estimated_fine += fine
        enriched_records.append({
            'txn': rec,
            'overdue_days': days,
            'fine': fine,
        })

    context = {
        'page_title': 'Overdue Books Monitor',
        'breadcrumb': 'Overdue Tracking',
        'records': enriched_records,
        'total_overdue': len(enriched_records),
        'total_estimated_fine': total_estimated_fine,
        'fine_per_day': settings.fine_per_day,
    }
    return render(request, 'library/librarian/overdue_monitor.html', context)


@librarian_required
def settle_fine_action(request, fine_id):
    if request.method != 'POST':
        return redirect('library:librarian_overdue')

    fine = get_object_or_404(Fine, id=fine_id)
    method = request.POST.get('payment_method', 'Cash')
    fine.is_settled = True
    fine.settled_at = timezone.now()
    fine.settled_by = request.user
    fine.payment_method = method
    fine.save()

    fine.transaction.fine_paid = True
    fine.transaction.save(update_fields=['fine_paid'])

    messages.success(request, f"Fine of ₹{fine.amount} for student {fine.student.enrollment_number} settled via {method}.")
    return redirect('library:librarian_overdue')
