from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from library.models import StudentProfile, LibraryRequest, CirculationTransaction, BookCopy
from library.decorators import student_required
from library.services.circulation_service import (
    create_book_request, cancel_book_request, request_book_return
)


def student_login_view(request):
    if request.user.is_authenticated and hasattr(request.user, 'library_student_profile'):
        return redirect('library:student_dashboard')

    if request.method == 'POST':
        identifier = request.POST.get('identifier', '').strip()
        password = request.POST.get('password', '').strip()

        profile = StudentProfile.objects.filter(enrollment_number__iexact=identifier).first()
        if not profile:
            profile = StudentProfile.objects.filter(library_card_number__iexact=identifier).first()

        username_to_try = profile.user.username if profile else identifier
        user = authenticate(request, username=username_to_try, password=password)

        if user is not None:
            if hasattr(user, 'library_student_profile'):
                login(request, user)
                messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
                next_url = request.GET.get('next') or 'library:student_dashboard'
                return redirect(next_url)
            else:
                messages.error(request, "This account is not registered as a Student Library Member.")
        else:
            messages.error(request, "Invalid Enrollment Number / Library Card Number or Password.")

    return render(request, 'library/student/login.html', {
        'page_title': 'Student Library Login',
        'breadcrumb': 'Student Authentication'
    })


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    next_url = request.GET.get('next') or 'library:home'
    return redirect(next_url)


def student_logout_view(request):
    return logout_view(request)


@student_required
def student_dashboard(request):
    profile = request.user.library_student_profile
    today = timezone.now().date()
    due_threshold = today + timedelta(days=3)

    issued_records = profile.circulation_records.filter(status__in=['ISSUED', 'RETURN_REQUESTED']).select_related('book_copy__book').order_by('due_date')
    pending_requests = profile.book_requests.filter(status__in=['PENDING', 'APPROVED']).select_related('book_copy__book')
    
    due_soon_count = sum(1 for rec in issued_records if rec.due_date <= due_threshold and not rec.is_overdue)
    overdue_count = sum(1 for rec in issued_records if rec.is_overdue)
    unsettled_fines = profile.fines.filter(is_settled=False)
    total_unpaid_fine = sum(f.amount for f in unsettled_fines)

    context = {
        'page_title': 'Student Library Dashboard',
        'breadcrumb': 'My Library Dashboard',
        'profile': profile,
        'issued_records': issued_records,
        'pending_requests': pending_requests,
        'due_soon_count': due_soon_count,
        'overdue_count': overdue_count,
        'total_unpaid_fine': total_unpaid_fine,
    }
    return render(request, 'library/student/dashboard.html', context)


@student_required
def my_requests(request):
    profile = request.user.library_student_profile
    requests_list = profile.book_requests.select_related('book_copy__book').order_by('-requested_at')

    context = {
        'page_title': 'My Book Requests',
        'breadcrumb': 'My Requests',
        'profile': profile,
        'requests_list': requests_list,
    }
    return render(request, 'library/student/my_requests.html', context)


@student_required
def my_issued_books(request):
    profile = request.user.library_student_profile
    issued_records = profile.circulation_records.filter(status__in=['ISSUED', 'RETURN_REQUESTED']).select_related('book_copy__book').order_by('due_date')

    context = {
        'page_title': 'Currently Issued Books',
        'breadcrumb': 'Issued Books',
        'profile': profile,
        'issued_records': issued_records,
    }
    return render(request, 'library/student/my_issued.html', context)


@student_required
def my_history(request):
    profile = request.user.library_student_profile
    past_records = profile.circulation_records.filter(status__in=['RETURNED', 'LOST', 'DAMAGED']).select_related('book_copy__book').order_by('-returned_at')
    fines = profile.fines.select_related('transaction__book_copy__book').order_by('-id')

    context = {
        'page_title': 'Borrowing & Circulation History',
        'breadcrumb': 'Circulation History',
        'profile': profile,
        'past_records': past_records,
        'fines': fines,
    }
    return render(request, 'library/student/my_history.html', context)


@student_required
def request_book_action(request):
    if request.method != 'POST':
        return redirect('library:catalogue')

    copy_id = request.POST.get('copy_id')
    remark = request.POST.get('remark', '').strip()
    profile = request.user.library_student_profile
    ip_addr = request.META.get('REMOTE_ADDR')

    try:
        req = create_book_request(profile, copy_id, remark=remark, ip_address=ip_addr)
        messages.success(request, f"Book request {req.request_number} submitted successfully! The library team will review your request.")
    except ValidationError as e:
        messages.error(request, str(e.message if hasattr(e, 'message') else e))
    except Exception as e:
        messages.error(request, f"Failed to submit request: {str(e)}")

    return redirect('library:my_requests')


@student_required
def cancel_request_action(request, request_id):
    if request.method != 'POST':
        return redirect('library:my_requests')

    profile = request.user.library_student_profile
    ip_addr = request.META.get('REMOTE_ADDR')

    try:
        cancel_book_request(profile, request_id, ip_address=ip_addr)
        messages.success(request, "Your book request has been cancelled.")
    except ValidationError as e:
        messages.error(request, str(e.message if hasattr(e, 'message') else e))
    except Exception as e:
        messages.error(request, f"Could not cancel request: {str(e)}")

    return redirect('library:my_requests')


@student_required
def return_request_action(request, transaction_id):
    if request.method != 'POST':
        return redirect('library:my_issued')

    profile = request.user.library_student_profile
    remark = request.POST.get('remark', '').strip()
    ip_addr = request.META.get('REMOTE_ADDR')

    try:
        request_book_return(profile, transaction_id, remark=remark, ip_address=ip_addr)
        messages.success(request, "Return request registered! Please bring the physical book to the library counter for receipt confirmation.")
    except ValidationError as e:
        messages.error(request, str(e.message if hasattr(e, 'message') else e))
    except Exception as e:
        messages.error(request, f"Failed to submit return request: {str(e)}")

    return redirect('library:my_issued')
