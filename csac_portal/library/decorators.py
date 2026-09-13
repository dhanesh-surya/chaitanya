from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def student_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Please log in with your Student account to access library services.")
            return redirect(f"/library/student/login/?next={request.path}")
        if not hasattr(request.user, 'library_student_profile'):
            messages.error(request, "Access restricted. You must have an active Student Library profile.")
            return redirect('library:catalogue')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def librarian_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Please log in with your staff or librarian credentials.")
            return redirect(f"/library/staff/login/?next={request.path}")
        is_librarian = hasattr(request.user, 'library_staff_profile')
        if not (is_librarian or request.user.is_staff or request.user.is_superuser):
            messages.error(request, "Access denied. Librarian privileges required.")
            return redirect('library:catalogue')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def library_admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Please log in to the administrator portal.")
            return redirect(f"/admin/login/?next={request.path}")
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, "Administrative privileges required.")
            return redirect('library:catalogue')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
