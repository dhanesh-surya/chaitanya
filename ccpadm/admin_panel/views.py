import csv
import re

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from accounts.models import AdminUser, Student
from accounts.utils import (
    admin_login_required,
    generate_secure_password,
    is_valid_aadhaar,
    is_valid_email,
    is_valid_mobile,
)
from admissions.models import StudentAdmission
from admissions.services import (
    get_print_context,
    parse_selected_subjects,
    parse_selected_subjects_payload,
)
from courses.subject_groups import (
    format_bsc_group_display_name,
    get_bsc_subject_group_sections,
    is_bsc_program,
)
from courses.utils import get_program_names

from .merit_list import (
    MERIT_EXPORT_HEADERS,
    STATUS_FILTER_CHOICES,
    build_merit_list_groups,
    build_merit_list_workbook,
    get_merit_program_choices,
    iter_merit_export_rows,
    merit_export_filename,
)


def _students_filter_params(request):
    """Read list filters from POST (actions) or GET (page load / filter form)."""
    if request.method == 'POST':
        source = request.POST
    else:
        source = request.GET

    program = (source.get('program') or '').strip()
    if program == 'ALL':
        program = ''
    verified = (source.get('verified') or 'ALL').strip() or 'ALL'
    group = (source.get('group') or 'ALL').strip() or 'ALL'
    return {
        'search': source.get('search', '').strip(),
        'program': program,
        'verified': verified,
        'group': group,
    }


def _subject_group_filter_choices(program_type):
    """B.Sc. subject groups for the selected program (empty when not B.Sc.)."""
    if not is_bsc_program(program_type):
        return []
    choices = []
    for section in get_bsc_subject_group_sections(program_type):
        for group in section['groups']:
            choices.append({
                'key': group['key'],
                'label': group.get('full_name') or f"{section['heading']} — {group['label']}",
            })
    return choices


def _normalize_group_filter(group_filter, program_type):
    """Drop invalid group keys when program is not B.Sc. or group is unknown."""
    group_filter = (group_filter or 'ALL').strip() or 'ALL'
    if group_filter == 'ALL':
        return 'ALL'
    choices = _subject_group_filter_choices(program_type)
    if not choices:
        return 'ALL'
    valid = {item['key'] for item in choices}
    if group_filter == 'NONE' or group_filter in valid:
        return group_filter
    return 'ALL'


def _admission_bsc_group_key(admission):
    if not admission:
        return ''
    _, group_key = parse_selected_subjects_payload(admission.selected_subjects_json)
    return (group_key or '').strip()


def _filter_students_by_group(students, group_filter='ALL'):
    if not group_filter or group_filter == 'ALL':
        return students
    result = []
    for student in students:
        key = _admission_bsc_group_key(getattr(student, 'latest_admission', None))
        if group_filter == 'NONE':
            if not key:
                result.append(student)
        elif key == group_filter:
            result.append(student)
    return result


def _students_url(params=None, edit_pk=None):
    from urllib.parse import urlencode
    from django.urls import reverse

    query = dict(params or {})
    if edit_pk:
        query['edit'] = edit_pk
    base = reverse('manage_students')
    if not query:
        return base
    return f'{base}?{urlencode(query)}'


def _get_students_queryset(search='', program_filter='', verified_filter='ALL'):
    if not program_filter and not search:
        return Student.objects.none()
    students = Student.objects.all()
    if search:
        students = students.filter(
            Q(full_name__icontains=search)
            | Q(email__icontains=search)
            | Q(mobile__icontains=search)
            | Q(registration_no__icontains=search)
            | Q(aadhaar__icontains=search)
        )
    if program_filter:
        students = students.filter(program_type=program_filter)
    if verified_filter == 'YES':
        students = students.filter(is_verified=True)
    elif verified_filter == 'NO':
        students = students.filter(is_verified=False)
    return students.order_by('-created_date')


def _export_course_name_only(label):
    """Strip B.Sc. department prefix; keep paper/course name only."""
    name = (label or '').strip()
    if not name:
        return ''
    if ' — ' in name:
        _department, course_name = name.split(' — ', 1)
        if course_name.strip():
            return course_name.strip()
    return name


def _format_selected_courses_for_export(student):
    """Paper names from the student's latest admission, for CSV export."""
    admission = getattr(student, 'latest_admission', None)
    if admission:
        subjects = parse_selected_subjects(admission)
        if subjects:
            names = [
                _export_course_name_only(s.get('name'))
                for s in subjects
                if isinstance(s, dict) and _export_course_name_only(s.get('name'))
            ]
            if names:
                return '; '.join(names)
        if (admission.subject or '').strip():
            names = [
                _export_course_name_only(part)
                for part in admission.subject.split(',')
                if _export_course_name_only(part)
            ]
            if names:
                return '; '.join(names)
    return _export_course_name_only(student.course_name)


def _admission_dsc_course_labels(admission):
    """DSC theory course labels from selected subjects (department — paper name)."""
    if not admission:
        return []
    subjects = parse_selected_subjects(admission)
    labels = []
    seen = set()
    for item in subjects:
        if not isinstance(item, dict):
            continue
        if (item.get('type2') or '').strip().upper() != 'DSC':
            continue
        type1 = (item.get('type1') or '').strip().lower()
        if 'practical' in type1 or 'lab' in type1:
            continue
        full = (item.get('name') or '').strip()
        if not full:
            continue
        key = full.lower()
        if key in seen:
            continue
        seen.add(key)
        labels.append(full)
    return labels


def _attach_admissions(students):
    reg_nos = [s.registration_no for s in students]
    admission_map = {}
    if reg_nos:
        for adm in (
            StudentAdmission.objects.filter(reg_no__in=reg_nos)
            .order_by('-submitted_date', '-created_date')
        ):
            if adm.reg_no not in admission_map:
                admission_map[adm.reg_no] = adm
    for student in students:
        admission = admission_map.get(student.registration_no)
        student.latest_admission = admission
        group_key = _admission_bsc_group_key(admission)
        student.bsc_group_key = group_key
        student.bsc_group_label = (
            format_bsc_group_display_name(group_key, student.program_type)
            if group_key
            else ''
        )
        student.dsc_course_names = _admission_dsc_course_labels(admission)
        student.dsc_courses_display = '; '.join(student.dsc_course_names)
    return students


def _program_group_label(program_type):
    label = (program_type or '').strip()
    return label or 'Not Assigned'


def _build_verified_students_by_program():
    """Group verified students by program (class) for admin dashboard."""
    verified = list(
        Student.objects.filter(is_verified=True).order_by('program_type', 'full_name', 'registration_no')
    )
    _attach_admissions(verified)

    groups = {}
    for student in verified:
        program = _program_group_label(student.program_type)
        groups.setdefault(program, []).append(student)

    return [
        {
            'program': program,
            'count': len(students),
            'students': students,
        }
        for program, students in sorted(
            groups.items(),
            key=lambda item: (item[0] == 'Not Assigned', item[0].lower()),
        )
    ]


_REJECTABLE_ADMISSION_STATUSES = ('Submitted', 'Pending', 'Approved')


def _get_latest_admission_for_student(student):
    return (
        StudentAdmission.objects.filter(reg_no=student.registration_no)
        .order_by('-submitted_date', '-created_date')
        .first()
    )


def _reject_student_application(student):
    admission = _get_latest_admission_for_student(student)
    if not admission or admission.status not in _REJECTABLE_ADMISSION_STATUSES:
        return False
    admission.status = 'Rejected'
    admission.save(update_fields=['status'])
    return True


def _validate_student_form(post, student=None):
    errors = []
    full_name = post.get('full_name', '').strip()
    email = post.get('email', '').strip().lower()
    mobile = re.sub(r'\D', '', post.get('mobile', '').strip())
    aadhaar = re.sub(r'\D', '', post.get('aadhaar', '').strip())
    program_type = post.get('program_type', '').strip()

    if not full_name:
        errors.append('Full name is required.')
    if email and not is_valid_email(email):
        errors.append('Invalid email format.')
    if mobile and not is_valid_mobile(mobile):
        errors.append('Invalid mobile number.')
    if aadhaar and not is_valid_aadhaar(aadhaar):
        errors.append('Invalid Aadhaar number.')

    if email:
        qs = Student.objects.filter(email__iexact=email)
        if student:
            qs = qs.exclude(pk=student.pk)
        if qs.exists():
            errors.append('Another student already uses this email.')

    if mobile:
        qs = Student.objects.filter(mobile=mobile)
        if student:
            qs = qs.exclude(pk=student.pk)
        if qs.exists():
            errors.append('Another student already uses this mobile.')

    if aadhaar:
        qs = Student.objects.filter(aadhaar=aadhaar)
        if student:
            qs = qs.exclude(pk=student.pk)
        if qs.exists():
            errors.append('Another student already uses this Aadhaar.')

    return errors, {
        'full_name': full_name,
        'email': email,
        'mobile': mobile,
        'aadhaar': aadhaar,
        'program_type': program_type,
        'course_name': post.get('course_name', '').strip(),
        'is_verified': post.get('is_verified') == 'on',
    }


@require_http_methods(['GET', 'POST'])
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        if AdminUser.objects.filter(username=username, password=password).exists():
            request.session['admin_user'] = username
            return redirect('admin_dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'admin_panel/login.html')


def admin_logout(request):
    request.session.pop('admin_user', None)
    return redirect('admin_login')


@admin_login_required
def admin_dashboard(request):
    from admissions.models import StudentEnrollment

    show_verified = request.GET.get('show_verified') == '1'
    verified_students = Student.objects.filter(is_verified=True).count()
    stats = {
        'total_admissions': StudentAdmission.objects.count(),
        'pending': StudentAdmission.objects.filter(status='Pending').count(),
        'approved': StudentAdmission.objects.filter(status='Approved').count(),
        'rejected': StudentAdmission.objects.filter(status='Rejected').count(),
        'submitted': StudentAdmission.objects.filter(status='Submitted').count(),
        'students': Student.objects.count(),
        'verified_students': verified_students,
        'total_enrollments': StudentEnrollment.objects.count(),
        'submitted_enrollments': StudentEnrollment.objects.filter(is_submitted=True).count(),
        'approved_enrollments': StudentEnrollment.objects.filter(status='Approved').count(),
    }
    recent = StudentAdmission.objects.order_by('-submitted_date', '-created_date')[:20]
    recent_enrollments = StudentEnrollment.objects.order_by('-submitted_date', '-created_at')[:20]
    return render(request, 'admin_panel/dashboard.html', {
        'stats': stats,
        'recent': recent,
        'recent_enrollments': recent_enrollments,
        'show_verified': show_verified,
        'verified_by_program': _build_verified_students_by_program() if show_verified else [],
    })


@admin_login_required
def manage_students(request):
    params = _students_filter_params(request)
    search = params['search']
    program_filter = params['program']
    verified_filter = params['verified']
    group_filter = _normalize_group_filter(params['group'], program_filter)
    params['group'] = group_filter
    edit_pk = request.GET.get('edit', '').strip()

    students = _filter_students_by_group(
        _attach_admissions(
            list(_get_students_queryset(search, program_filter, verified_filter))
        ),
        group_filter,
    )

    edit_student = None
    if edit_pk:
        edit_student = Student.objects.filter(pk=edit_pk).first()
        if edit_student:
            _attach_admissions([edit_student])

    program_types = get_program_names(active_only=False)
    subject_group_choices = _subject_group_filter_choices(program_filter)
    show_group_filter = bool(subject_group_choices)
    reset_password_display = request.session.pop('reset_password_display', None)
    bulk_reset_passwords_display = request.session.pop('bulk_reset_passwords_display', None)

    return render(request, 'admin_panel/students.html', {
        'students': students,
        'search': search,
        'program_filter': program_filter,
        'verified_filter': verified_filter,
        'group_filter': group_filter,
        'program_types': program_types,
        'subject_group_choices': subject_group_choices,
        'show_group_filter': show_group_filter,
        'edit_student': edit_student,
        'filter_params': params,
        'total_count': len(students),
        'reset_password_display': reset_password_display,
        'bulk_reset_passwords_display': bulk_reset_passwords_display,
    })


@admin_login_required
@require_http_methods(['POST'])
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    errors, data = _validate_student_form(request.POST, student=student)
    params = _students_filter_params(request)

    if errors:
        for err in errors:
            messages.error(request, err)
        return redirect(_students_url(params, edit_pk=pk))

    student.full_name = data['full_name']
    student.email = data['email'] or None
    student.mobile = data['mobile'] or None
    student.aadhaar = data['aadhaar'] or None
    student.program_type = data['program_type']
    student.course_name = data['course_name']
    student.is_verified = data['is_verified']
    student.save()
    messages.success(request, f'Student {student.registration_no} updated successfully.')
    return redirect(_students_url(params))


@admin_login_required
@require_http_methods(['POST'])
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    params = _students_filter_params(request)

    if StudentAdmission.objects.filter(reg_no=student.registration_no, status='Submitted').exists():
        messages.error(
            request,
            f'Cannot delete {student.registration_no} — reject the submitted application first.',
        )
        return redirect(_students_url(params))

    reg_no = student.registration_no
    StudentAdmission.objects.filter(reg_no=reg_no).delete()
    student.delete()
    messages.success(request, f'Student {reg_no} deleted.')
    return redirect(_students_url(params))


@admin_login_required
@require_http_methods(['POST'])
def reset_student_password(request, pk):
    student = get_object_or_404(Student, pk=pk)
    params = _students_filter_params(request)
    new_password = generate_secure_password()
    student.password = new_password
    student.save(update_fields=['password'])
    request.session['reset_password_display'] = {
        'registration_no': student.registration_no,
        'password': new_password,
    }
    messages.success(request, f'Password reset for {student.registration_no}.')
    return redirect(_students_url(params))


def _unverify_and_reassign_student(student):
    """
    Mark student as unverified and reset their latest admission status to 'Draft'
    so they can completely edit their form.
    """
    student.is_verified = False
    student.save(update_fields=['is_verified'])

    from admissions.models import StudentAdmission
    admission = (
        StudentAdmission.objects.filter(reg_no=student.registration_no)
        .order_by('-submitted_date', '-created_date')
        .first()
    )
    if admission:
        admission.status = 'Draft'
        admission.is_submitted = False
        admission.is_approved = False
        admission.save(update_fields=['status', 'is_submitted', 'is_approved'])


def _verify_student(student):
    """
    Mark student as verified and approve their latest admission.
    """
    student.is_verified = True
    student.save(update_fields=['is_verified'])

    from admissions.models import StudentAdmission
    admission = (
        StudentAdmission.objects.filter(reg_no=student.registration_no)
        .order_by('-submitted_date', '-created_date')
        .first()
    )
    if admission:
        admission.status = 'Approved'
        admission.is_submitted = True
        admission.is_approved = True
        admission.save(update_fields=['status', 'is_submitted', 'is_approved'])


@admin_login_required
@require_http_methods(['POST'])
def toggle_student_verified(request, pk):
    student = get_object_or_404(Student, pk=pk)
    params = _students_filter_params(request)
    if student.is_verified:
        _unverify_and_reassign_student(student)
        messages.success(request, f'{student.registration_no} marked as unverified and reassigned to Draft status.')
    else:
        _verify_student(student)
        messages.success(request, f'{student.registration_no} marked as verified and application approved.')
    return redirect(_students_url(params))


@admin_login_required
@require_http_methods(['POST'])
def bulk_student_action(request):
    valid_actions = ('verify', 'unverify', 'reset_password', 'reject_application', 'delete')
    params = _students_filter_params(request)
    raw_ids = request.POST.getlist('student_ids')
    student_ids = []
    for raw_id in raw_ids:
        try:
            student_ids.append(int(raw_id))
        except (TypeError, ValueError):
            continue

    action = request.POST.get('action', '').strip()
    if not student_ids:
        messages.error(request, 'Select at least one student.')
        return redirect(_students_url(params))
    if action not in valid_actions:
        messages.error(request, 'Choose a valid action.')
        return redirect(_students_url(params))

    students = list(Student.objects.filter(pk__in=student_ids))
    if not students:
        messages.error(request, 'No matching students found.')
        return redirect(_students_url(params))

    if action == 'verify':
        for student in students:
            _verify_student(student)
        messages.success(
            request,
            f'Marked {len(students)} student{"s" if len(students) != 1 else ""} as verified and approved their applications.',
        )
    elif action == 'unverify':
        for student in students:
            _unverify_and_reassign_student(student)
        messages.success(
            request,
            f'Marked {len(students)} student{"s" if len(students) != 1 else ""} as not verified and reassigned to Draft status.',
        )
    elif action == 'reset_password':
        reset_list = []
        for student in students:
            new_password = generate_secure_password()
            student.password = new_password
            student.save(update_fields=['password'])
            reset_list.append({
                'registration_no': student.registration_no,
                'password': new_password,
            })
        request.session['bulk_reset_passwords_display'] = reset_list
        messages.success(
            request,
            f'Reset password for {len(reset_list)} student{"s" if len(reset_list) != 1 else ""}.',
        )
    elif action == 'reject_application':
        rejected = 0
        skipped = []
        for student in students:
            if _reject_student_application(student):
                rejected += 1
            else:
                skipped.append(student.registration_no)
        if rejected:
            messages.success(
                request,
                f'Rejected {rejected} application{"s" if rejected != 1 else ""}. '
                'Those students can now be deleted.',
            )
        if skipped:
            messages.warning(
                request,
                'Skipped '
                f'{len(skipped)} student{"s" if len(skipped) != 1 else ""} with no rejectable application: '
                + ', '.join(skipped),
            )
        if not rejected and not skipped:
            messages.error(request, 'No applications were rejected.')
    elif action == 'delete':
        deleted = 0
        skipped = []
        for student in students:
            if StudentAdmission.objects.filter(
                reg_no=student.registration_no,
                status='Submitted',
            ).exists():
                skipped.append(student.registration_no)
                continue
            reg_no = student.registration_no
            StudentAdmission.objects.filter(reg_no=reg_no).delete()
            student.delete()
            deleted += 1
        if deleted:
            messages.success(
                request,
                f'Deleted {deleted} student{"s" if deleted != 1 else ""}.',
            )
        if skipped:
            messages.warning(
                request,
                'Skipped '
                f'{len(skipped)} student{"s" if len(skipped) != 1 else ""} with submitted applications '
                '(reject the application first): '
                + ', '.join(skipped),
            )
        if not deleted and not skipped:
            messages.error(request, 'No students were deleted.')

    return redirect(_students_url(params))


def _merit_list_params(request):
    program = request.GET.get('program', 'ALL').strip() or 'ALL'
    status = request.GET.get('status', 'applied').strip() or 'applied'
    valid_statuses = {key for key, _ in STATUS_FILTER_CHOICES}
    if status not in valid_statuses:
        status = 'applied'
    return {'program': program, 'status': status}


@admin_login_required
def merit_list(request):
    params = _merit_list_params(request)
    program_filter = params['program']
    status_filter = params['status']
    groups = build_merit_list_groups(program_filter, status_filter)
    total_applications = sum(group['count'] for group in groups)

    return render(request, 'admin_panel/merit_list.html', {
        'groups': groups,
        'program_filter': program_filter,
        'status_filter': status_filter,
        'program_choices': get_merit_program_choices(status_filter),
        'status_choices': STATUS_FILTER_CHOICES,
        'total_applications': total_applications,
    })


@admin_login_required
def export_merit_list_csv(request):
    params = _merit_list_params(request)
    groups = build_merit_list_groups(params['program'], params['status'])

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = (
        f'attachment; filename="{merit_export_filename(params["program"], "csv")}"'
    )
    writer = csv.writer(response)
    writer.writerow(MERIT_EXPORT_HEADERS)
    for row in iter_merit_export_rows(groups):
        writer.writerow(row)
    return response


@admin_login_required
def export_merit_list_excel(request):
    params = _merit_list_params(request)
    groups = build_merit_list_groups(params['program'], params['status'])
    workbook = build_merit_list_workbook(
        groups,
        program_filter=params['program'],
        status_filter=params['status'],
    )

    response = HttpResponse(
        workbook.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = (
        f'attachment; filename="{merit_export_filename(params["program"], "xlsx")}"'
    )
    return response


@admin_login_required
def export_students_csv(request):
    params = _students_filter_params(request)
    if not params['program'] and not params['search']:
        messages.warning(request, 'Please select a program before exporting CSV.')
        return redirect('manage_students')
    group_filter = _normalize_group_filter(params['group'], params['program'])
    students = _filter_students_by_group(
        _attach_admissions(
            list(_get_students_queryset(params['search'], params['program'], params['verified']))
        ),
        group_filter,
    )

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'Registration No', 'Full Name', 'Email', 'Mobile', 'Aadhaar',
        'Program', 'Subject Group', 'DSC Courses', 'Course', 'Selected Courses / Paper Name',
        'Application No', 'Verified', 'Registered On',
    ])
    for s in students:
        admission = getattr(s, 'latest_admission', None)
        writer.writerow([
            s.registration_no,
            s.full_name,
            s.email or '',
            s.mobile or '',
            s.aadhaar or '',
            s.program_type,
            getattr(s, 'bsc_group_label', '') or '',
            getattr(s, 'dsc_courses_display', '') or '',
            s.course_name,
            _format_selected_courses_for_export(s),
            (admission.application_no if admission else '') or '',
            'Yes' if s.is_verified else 'No',
            s.created_date.strftime('%d-%m-%Y %H:%M') if s.created_date else '',
        ])
    return response


@admin_login_required
def admin_print_application(request, app_no):
    admission = get_object_or_404(StudentAdmission, application_no=app_no)
    context = get_print_context(admission)
    context['preview_mode'] = False
    context['admin_view'] = True
    return render(request, 'admissions/print_full.html', context)


@admin_login_required
def admin_download_pdf(request, app_no):
    from admissions.pdf import render_admission_pdf

    admission = get_object_or_404(StudentAdmission, application_no=app_no)
    pdf_bytes = render_admission_pdf(admission)
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{app_no}.pdf"'
    return response


@admin_login_required
@require_http_methods(['POST'])
def update_admission_status(request, pk):
    admission = StudentAdmission.objects.filter(pk=pk).first()
    if not admission:
        messages.error(request, 'Admission not found.')
        return redirect('admin_dashboard')
    new_status = request.POST.get('status')
    if new_status in ('Approved', 'Rejected', 'Pending', 'Submitted', 'Draft'):
        admission.status = new_status
        if new_status == 'Draft':
            admission.is_submitted = False
            admission.is_approved = False
            admission.save(update_fields=['status', 'is_submitted', 'is_approved'])
            student = Student.objects.filter(registration_no=admission.reg_no).first()
            if student:
                student.is_verified = False
                student.save(update_fields=['is_verified'])
            messages.success(request, 'Application status reset to Draft (Unverified, editable by student).')
        else:
            admission.save(update_fields=['status'])
            if new_status == 'Approved':
                student = Student.objects.filter(registration_no=admission.reg_no).first()
                if student:
                    student.is_verified = True
                    student.save(update_fields=['is_verified'])
            messages.success(request, f'Status updated to {new_status}.')
    return redirect(request.POST.get('next', 'admin_dashboard'))


@admin_login_required
@require_http_methods(['POST'])
def bulk_update_admission_status(request):
    valid_statuses = ('Approved', 'Rejected', 'Pending', 'Submitted', 'Draft')
    raw_ids = request.POST.getlist('admission_ids')
    admission_ids = []
    for raw_id in raw_ids:
        try:
            admission_ids.append(int(raw_id))
        except (TypeError, ValueError):
            continue

    new_status = request.POST.get('status', '').strip()
    if not admission_ids:
        messages.error(request, 'Select at least one application.')
        return redirect('admin_dashboard')
    if new_status not in valid_statuses:
        messages.error(request, 'Choose a valid status.')
        return redirect('admin_dashboard')

    admissions = StudentAdmission.objects.filter(pk__in=admission_ids)
    if new_status == 'Draft':
        updated = 0
        for adm in admissions:
            adm.status = 'Draft'
            adm.is_submitted = False
            adm.is_approved = False
            adm.save(update_fields=['status', 'is_submitted', 'is_approved'])
            Student.objects.filter(registration_no=adm.reg_no).update(is_verified=False)
            updated += 1
    else:
        updated = admissions.update(status=new_status)
        if new_status == 'Approved':
            reg_nos = admissions.values_list('reg_no', flat=True)
            Student.objects.filter(registration_no__in=reg_nos).update(is_verified=True)

    if updated:
        messages.success(
            request,
            f'Updated {updated} application{"s" if updated != 1 else ""} to {new_status}.',
        )
    else:
        messages.error(request, 'No matching applications found.')
    return redirect('admin_dashboard')


@admin_login_required
@require_http_methods(['POST'])
def update_enrollment_status(request, pk):
    from admissions.models import StudentEnrollment
    from admissions.utils import generate_enrollment_number

    enrollment = get_object_or_404(StudentEnrollment, pk=pk)
    new_status = request.POST.get('status', '').strip()
    if new_status in ('Approved', 'Submitted', 'Draft'):
        enrollment.status = new_status
        if new_status == 'Approved':
            enrollment.is_submitted = True
            if not enrollment.enrollment_no:
                enrollment.enrollment_no = generate_enrollment_number()
            enrollment.save(update_fields=['status', 'is_submitted', 'enrollment_no'])
            Student.objects.filter(registration_no=enrollment.reg_no).update(is_verified=True)
            messages.success(request, f'Enrollment {enrollment.enrollment_no} for {enrollment.full_name} has been Approved / Accepted.')
        elif new_status == 'Draft':
            enrollment.is_submitted = False
            enrollment.save(update_fields=['status', 'is_submitted'])
            messages.success(request, f'Enrollment {enrollment.enrollment_no or enrollment.reg_no} for {enrollment.full_name} reset to Draft (student can now edit).')
        else:
            enrollment.save(update_fields=['status'])
            messages.success(request, f'Enrollment status updated to {new_status}.')
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'admin_dashboard'
    return redirect(next_url)


@admin_login_required
@require_http_methods(['POST'])
def bulk_update_enrollment_status(request):
    from admissions.models import StudentEnrollment
    from admissions.utils import generate_enrollment_number

    enrollment_ids = request.POST.getlist('enrollment_ids')
    new_status = request.POST.get('status', '').strip()
    valid_statuses = ('Approved', 'Draft')

    if not enrollment_ids:
        messages.error(request, 'Select at least one enrollment application.')
        return redirect(request.META.get('HTTP_REFERER') or 'admin_dashboard')
    if new_status not in valid_statuses:
        messages.error(request, 'Choose a valid status (Approve or Reset to Draft).')
        return redirect(request.META.get('HTTP_REFERER') or 'admin_dashboard')

    enrollments = StudentEnrollment.objects.filter(pk__in=enrollment_ids)
    count = 0
    if new_status == 'Approved':
        for enr in enrollments:
            enr.status = 'Approved'
            enr.is_submitted = True
            if not enr.enrollment_no:
                enr.enrollment_no = generate_enrollment_number()
            enr.save(update_fields=['status', 'is_submitted', 'enrollment_no'])
            Student.objects.filter(registration_no=enr.reg_no).update(is_verified=True)
            count += 1
        messages.success(request, f'Successfully Approved & Accepted {count} enrollment application(s).')
    elif new_status == 'Draft':
        for enr in enrollments:
            enr.status = 'Draft'
            enr.is_submitted = False
            enr.save(update_fields=['status', 'is_submitted'])
            count += 1
        messages.success(request, f'Reset {count} enrollment application(s) to Draft (students can now edit).')

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'admin_dashboard'
    return redirect(next_url)


@admin_login_required
def manage_enrollments(request):
    from admissions.models import StudentEnrollment

    search = request.GET.get('search', '').strip()
    program_filter = request.GET.get('program', '').strip()
    if program_filter == 'ALL':
        program_filter = ''
    status_filter = request.GET.get('status', 'ALL').strip() or 'ALL'

    enrollments = StudentEnrollment.objects.all().select_related('student')

    if search:
        enrollments = enrollments.filter(
            Q(full_name__icontains=search)
            | Q(reg_no__icontains=search)
            | Q(enrollment_no__icontains=search)
            | Q(mobile__icontains=search)
            | Q(email__icontains=search)
        )

    if program_filter:
        enrollments = enrollments.filter(program_type=program_filter)

    if status_filter != 'ALL':
        enrollments = enrollments.filter(status=status_filter)

    total_count = StudentEnrollment.objects.count()
    submitted_count = StudentEnrollment.objects.filter(status='Submitted').count()
    approved_count = StudentEnrollment.objects.filter(status='Approved').count()
    draft_count = StudentEnrollment.objects.filter(status='Draft').count()

    program_types = get_program_names(active_only=False)

    return render(request, 'admin_panel/enrollments.html', {
        'enrollments': enrollments,
        'search': search,
        'program_filter': program_filter,
        'status_filter': status_filter,
        'program_types': program_types,
        'total_count': total_count,
        'submitted_count': submitted_count,
        'approved_count': approved_count,
        'draft_count': draft_count,
        'filtered_count': enrollments.count(),
    })


def _format_enrollment_address(enrollment):
    perm_parts = [
        enrollment.perm_village,
        enrollment.perm_city,
        enrollment.perm_district,
        enrollment.perm_state,
        enrollment.perm_pin_code,
    ]
    parts = []
    for p in perm_parts:
        val = (p or '').strip()
        if val and (not parts or val.lower() != parts[-1].lower()):
            parts.append(val)

    if not parts:
        corr_parts = [
            enrollment.corr_village,
            enrollment.corr_city,
            enrollment.corr_district,
            enrollment.corr_state,
            enrollment.corr_pin_code,
        ]
        for p in corr_parts:
            val = (p or '').strip()
            if val and (not parts or val.lower() != parts[-1].lower()):
                parts.append(val)

    if not parts and enrollment.admission:
        adm = enrollment.admission
        adm_parts = [
            adm.perm_village,
            adm.perm_city,
            adm.perm_district,
            adm.perm_state,
            adm.perm_pin_code,
        ]
        for p in adm_parts:
            val = (p or '').strip()
            if val and (not parts or val.lower() != parts[-1].lower()):
                parts.append(val)

    return ', '.join(parts)


def _format_enrollment_gender(gender_val):
    if not gender_val:
        return ''
    g = str(gender_val).strip().lower()
    if g.startswith('m') or g in ('1', 'male'):
        return 1
    elif g.startswith('f') or g in ('0', 'female'):
        return 0
    return gender_val


def _format_enrollment_dob(dob_val):
    if not dob_val:
        return ''
    if hasattr(dob_val, 'strftime'):
        return dob_val.strftime('%m/%d/%Y')
    return str(dob_val)


def _format_enrollment_subject_codes(enrollment):
    import json
    from courses.models import ProgramCourse

    courses = []
    if enrollment.selected_courses_json:
        try:
            data = json.loads(enrollment.selected_courses_json)
            if isinstance(data, list):
                courses = data
            elif isinstance(data, dict):
                courses = data.get('courses') or data.get('subjects') or []
        except Exception:
            courses = []

    codes = []
    for c in courses:
        if not isinstance(c, dict):
            continue
        code = (c.get('code') or c.get('course_code') or '').strip()
        name = (c.get('name') or c.get('course_name') or '').strip()
        dept = (c.get('dept') or c.get('department') or '').strip()
        type_2 = (c.get('type_2') or c.get('type2') or '').strip()

        # If code was missing in JSON, resolve it from ProgramCourse
        if not code and name:
            clean_name = name.split('—')[-1].strip() if '—' in name else name
            db_c = ProgramCourse.objects.filter(program_type__iexact=enrollment.program_type).filter(
                Q(course_name__iexact=name) | Q(course_name__iexact=clean_name)
            ).first()
            if not db_c and dept:
                db_c = ProgramCourse.objects.filter(
                    program_type__iexact=enrollment.program_type,
                    department__iexact=dept,
                    course_type_2__iexact=type_2,
                ).first()
            if db_c and db_c.course_code:
                code = db_c.course_code.strip()

        if code and code not in codes:
            codes.append(code)

    return ', '.join(codes)


def _format_enrollment_subjects(enrollment):
    import json
    courses = []
    if enrollment.selected_courses_json:
        try:
            data = json.loads(enrollment.selected_courses_json)
            if isinstance(data, list):
                courses = data
            elif isinstance(data, dict):
                courses = data.get('courses') or data.get('subjects') or []
        except Exception:
            courses = []

    names = []
    for c in courses:
        raw_name = ''
        if isinstance(c, dict):
            raw_name = c.get('name') or c.get('course_name') or ''
        elif isinstance(c, str):
            raw_name = c
        if raw_name:
            clean = _export_course_name_only(raw_name)
            if clean and clean not in names:
                names.append(clean)

    if names:
        return ', '.join(names)

    adm = enrollment.admission
    if not adm and enrollment.reg_no:
        from admissions.models import StudentAdmission
        adm = StudentAdmission.objects.filter(reg_no=enrollment.reg_no).first()

    if adm and (adm.subject or '').strip():
        parts = [_export_course_name_only(p) for p in adm.subject.split(',') if _export_course_name_only(p)]
        return ', '.join(parts)

    return ''


def build_enrollment_export_row(enrollment):
    adm = enrollment.admission
    if not adm and enrollment.reg_no:
        from admissions.models import StudentAdmission
        adm = StudentAdmission.objects.filter(reg_no=enrollment.reg_no).first()

    admission_no = (getattr(adm, 'application_no', '') or enrollment.reg_no or '').strip()
    univ_enrol_no = enrollment.enrollment_no or ''
    stud_nm = enrollment.full_name or (enrollment.student.full_name if enrollment.student else '')
    father_name = enrollment.father_name or (getattr(adm, 'father_name', '') or '')
    mother_name = enrollment.mother_name or (getattr(adm, 'mother_name', '') or '')
    medium = enrollment.medium or (getattr(adm, 'medium', '') or '')
    category = enrollment.category or (getattr(adm, 'category', '') or '')

    gender_raw = enrollment.gender or (getattr(adm, 'gender', '') or '')
    gender_val = _format_enrollment_gender(gender_raw)

    dob_raw = enrollment.dob or (getattr(adm, 'dob', None))
    dob_val = _format_enrollment_dob(dob_raw)

    address = _format_enrollment_address(enrollment)
    mobile = enrollment.mobile or (enrollment.student.mobile if enrollment.student else '')
    class_name = enrollment.program_type or ''
    subject_codes = _format_enrollment_subject_codes(enrollment)
    subjects = _format_enrollment_subjects(enrollment)

    return [
        admission_no,
        univ_enrol_no,
        stud_nm,
        father_name,
        mother_name,
        medium,
        category,
        gender_val,
        dob_val,
        address,
        mobile,
        class_name,
        subject_codes,
        subjects,
    ]


@admin_login_required
def export_enrollments_excel(request):
    """Export student enrollments as an Excel (.xlsx) spreadsheet matching university format."""
    from io import BytesIO
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    from admissions.models import StudentEnrollment

    search = request.GET.get('search', '').strip()
    program_filter = request.GET.get('program', '').strip()
    if program_filter == 'ALL':
        program_filter = ''
    status_filter = request.GET.get('status', 'ALL').strip() or 'ALL'

    enrollments = StudentEnrollment.objects.all().select_related('student', 'admission')

    if search:
        enrollments = enrollments.filter(
            Q(full_name__icontains=search)
            | Q(reg_no__icontains=search)
            | Q(enrollment_no__icontains=search)
            | Q(mobile__icontains=search)
            | Q(email__icontains=search)
        )

    if program_filter:
        enrollments = enrollments.filter(program_type=program_filter)

    if status_filter != 'ALL':
        enrollments = enrollments.filter(status=status_filter)

    enrollments = enrollments.order_by('program_type', 'enrollment_no', 'full_name')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Enrollments'
    ws.views.sheetView[0].showGridLines = True

    headers = [
        'AddmissionNo',
        'Univ_EnrolNo',
        'Stud_nm',
        'FatherName',
        'MotherName',
        'Medium',
        'Category',
        'Gender (MALE-1 ,FEMALE-0)',
        'DOB (MM/DD/YYYY)',
        'Address',
        'Mobile',
        'CLASS NAME',
        'SUBJECT CODE',
        'SUBJECTS',
    ]

    header_font = Font(name='Calibri', size=11, bold=True, color='FFFFFF')
    header_fill = PatternFill('solid', fgColor='082B49')
    center_align = Alignment(horizontal='center', vertical='center')
    left_align = Alignment(horizontal='left', vertical='center')
    thin_border = Border(
        left=Side(style='thin', color='D1D5DB'),
        right=Side(style='thin', color='D1D5DB'),
        top=Side(style='thin', color='D1D5DB'),
        bottom=Side(style='thin', color='D1D5DB'),
    )

    ws.row_dimensions[1].height = 28
    for col_idx, header in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align
        cell.border = thin_border

    row_num = 2
    for enr in enrollments:
        row_data = build_enrollment_export_row(enr)
        ws.row_dimensions[row_num].height = 20
        for col_idx, val in enumerate(row_data, start=1):
            cell = ws.cell(row=row_num, column=col_idx, value=val)
            cell.font = Font(name='Calibri', size=10)
            cell.border = thin_border
            if col_idx in (8, 9, 11):  # Gender, DOB, Mobile
                cell.alignment = center_align
            else:
                cell.alignment = left_align
        row_num += 1

    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = max(len(str(cell.value or '')) for cell in col)
        ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

    if ws.column_dimensions.get('J'):
        ws.column_dimensions['J'].width = min(max(ws.column_dimensions['J'].width, 30), 50)
    if ws.column_dimensions.get('M'):
        ws.column_dimensions['M'].width = min(max(ws.column_dimensions['M'].width, 24), 45)
    if ws.column_dimensions.get('N'):
        ws.column_dimensions['N'].width = min(max(ws.column_dimensions['N'].width, 35), 65)

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    filename_parts = ['enrollments']
    if program_filter:
        safe_prog = re.sub(r'[^\w\-]+', '_', program_filter).strip('_')
        filename_parts.append(safe_prog)
    if status_filter != 'ALL':
        filename_parts.append(status_filter.lower())
    filename_parts.append(timezone.now().strftime('%Y%m%d'))
    filename = f"{'_'.join(filename_parts)}.xlsx"

    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response