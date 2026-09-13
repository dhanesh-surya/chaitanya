import csv
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from library.models import (
    Book, BookCopy, CirculationTransaction, StudentProfile, LibrarySetting, AuditLog, ExcelImport
)
from library.decorators import library_admin_required
from library.services.excel_import_service import (
    parse_rows_from_file, validate_import_data, commit_import_records
)


@library_admin_required
def admin_dashboard(request):
    total_books = Book.objects.filter(is_active=True).count()
    total_copies = BookCopy.objects.filter(is_active=True).count()
    issued_copies = BookCopy.objects.filter(is_active=True, status='ISSUED').count()
    available_copies = BookCopy.objects.filter(is_active=True, status='AVAILABLE').count()
    
    today = timezone.now().date()
    overdue_count = CirculationTransaction.objects.filter(
        status__in=['ISSUED', 'RETURN_REQUESTED'],
        due_date__lt=today
    ).count()

    total_students = StudentProfile.objects.count()
    active_students = StudentProfile.objects.filter(status='ACTIVE', is_library_eligible=True).count()

    recent_imports = ExcelImport.objects.all().order_by('-uploaded_at')[:5]
    recent_audits = AuditLog.objects.all().order_by('-timestamp')[:10]

    context = {
        'page_title': 'Library Administration',
        'breadcrumb': 'Admin Control Panel',
        'total_books': total_books,
        'total_copies': total_copies,
        'issued_copies': issued_copies,
        'available_copies': available_copies,
        'overdue_count': overdue_count,
        'total_students': total_students,
        'active_students': active_students,
        'recent_imports': recent_imports,
        'recent_audits': recent_audits,
    }
    return render(request, 'library/admin/dashboard.html', context)


@library_admin_required
def import_excel_view(request):
    preview_data = None
    if request.method == 'POST' and request.FILES.get('excel_file'):
        file_obj = request.FILES['excel_file']
        try:
            headers, raw_rows = parse_rows_from_file(file_obj)
            validation_res = validate_import_data(raw_rows)
            
            # Store in session for confirmation
            request.session['import_valid_rows'] = validation_res['valid_rows']
            request.session['import_file_name'] = file_obj.name

            preview_data = {
                'file_name': file_obj.name,
                'total_rows': validation_res['total_rows'],
                'valid_count': validation_res['valid_count'],
                'error_count': validation_res['error_count'],
                'sample_valid': validation_res['valid_rows'][:10],
                'sample_errors': validation_res['error_rows'][:20],
            }
        except Exception as e:
            messages.error(request, f"Error processing file: {str(e)}")

    context = {
        'page_title': 'Import Books from Excel / CSV',
        'breadcrumb': 'Batch Book Importer',
        'preview_data': preview_data,
    }
    return render(request, 'library/admin/import_excel.html', context)


@library_admin_required
def import_commit_action(request):
    if request.method != 'POST':
        return redirect('library:admin_import')

    valid_rows = request.session.get('import_valid_rows', [])
    file_name = request.session.get('import_file_name', 'upload.xlsx')
    ip_addr = request.META.get('REMOTE_ADDR')

    if not valid_rows:
        messages.error(request, "No validated rows available to import. Please re-upload your file.")
        return redirect('library:admin_import')

    try:
        result = commit_import_records(
            valid_rows,
            uploaded_by_user=request.user,
            file_name=file_name,
            ip_address=ip_addr
        )
        # Clear session
        request.session.pop('import_valid_rows', None)
        request.session.pop('import_file_name', None)

        messages.success(request, f"Successfully imported {result['created_copies']} copies ({result['created_books']} new titles) into the library database!")
        return redirect('library:catalogue')
    except Exception as e:
        messages.error(request, f"Failed to commit import to database: {str(e)}")
        return redirect('library:admin_import')


@library_admin_required
def rules_settings_view(request):
    settings = LibrarySetting.get_settings()

    if request.method == 'POST':
        try:
            settings.max_books_per_student = int(request.POST.get('max_books_per_student', 3))
            settings.default_loan_days = int(request.POST.get('default_loan_days', 14))
            settings.fine_per_day = float(request.POST.get('fine_per_day', 2.0))
            settings.max_renewals = int(request.POST.get('max_renewals', 1))
            settings.max_pending_requests = int(request.POST.get('max_pending_requests', 2))
            settings.request_expiry_days = int(request.POST.get('request_expiry_days', 3))
            settings.allow_borrowing_if_fines = request.POST.get('allow_borrowing_if_fines') == 'on'
            settings.save()
            messages.success(request, "Library circulation rules updated successfully!")
        except Exception as e:
            messages.error(request, f"Failed to update rules: {str(e)}")

    context = {
        'page_title': 'Library Rules & Circulation Settings',
        'breadcrumb': 'Circulation Rules',
        'settings': settings,
    }
    return render(request, 'library/admin/rules_settings.html', context)


@library_admin_required
def audit_logs_view(request):
    action_filter = request.GET.get('action', '')
    search_q = request.GET.get('q', '').strip()

    logs = AuditLog.objects.select_related('user').order_by('-timestamp')
    if action_filter:
        logs = logs.filter(action=action_filter)
    if search_q:
        logs = logs.filter(reference_id__icontains=search_q)

    context = {
        'page_title': 'Library Audit Trail',
        'breadcrumb': 'Audit Logs',
        'logs': logs[:200],
        'action_choices': AuditLog.ACTION_CHOICES,
        'selected_action': action_filter,
        'search_q': search_q,
    }
    return render(request, 'library/admin/audit_logs.html', context)


@library_admin_required
def circulation_reports_view(request):
    today = timezone.now().date()
    txns = CirculationTransaction.objects.select_related('student__user', 'book_copy__book').order_by('-issued_at')

    # Export to CSV if requested
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="circulation_report_{today}.csv"'
        writer = csv.writer(response)
        writer.writerow(['Transaction No', 'Student Name', 'Enrollment No', 'Book Title', 'Accession No', 'Issue Date', 'Due Date', 'Return Date', 'Status', 'Fine (Rs)'])
        for t in txns:
            writer.writerow([
                t.transaction_number,
                t.student.full_name,
                t.student.enrollment_number,
                t.book_copy.book.title,
                t.book_copy.accession_number,
                t.issued_at.strftime('%Y-%m-%d'),
                t.due_date.strftime('%Y-%m-%d'),
                t.returned_at.strftime('%Y-%m-%d') if t.returned_at else '',
                t.get_status_display(),
                t.fine_amount
            ])
        return response

    context = {
        'page_title': 'Library Circulation Reports',
        'breadcrumb': 'Reports & Analytics',
        'transactions': txns[:100],
    }
    return render(request, 'library/admin/reports.html', context)
