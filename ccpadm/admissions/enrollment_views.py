import json
import logging

from django.db import models
from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from accounts.models import Student
from accounts.utils import get_student_sidebar_context, student_login_required
from courses.constants import PROGRAM_LEVEL_CHOICES, PROGRAM_LEVEL_DISPLAY
from courses.instructions import get_program_course_instructions
from courses.models import Program, ProgramCourse
from courses.subject_groups import (
    BSC_PROGRAM,
    get_bsc_subject_group_sections,
    is_bsc_program,
    normalize_program_type_for_display,
)
from courses.utils import (
    get_program_level_for_name,
    get_program_names,
    get_programs_by_level,
)
from admissions.services import build_education_list, parse_selected_subjects_payload

from .constants import MEDIUM_CHOICES, RELIGION_CHOICES
from .models import StudentAdmission, StudentEnrollment
from .utils import generate_enrollment_number

logger = logging.getLogger(__name__)


def _normalize_program_name(name):
    name = (name or '').strip()
    if name and not name.endswith('First Semester') and ('B.' in name or 'BBA' in name or 'BCA' in name):
        # Check if there is a 'First Semester' counterpart
        candidate = f'{name} First Semester'
        if Program.objects.filter(program_name__iexact=candidate).exists() or ProgramCourse.objects.filter(program_type__iexact=candidate).exists():
            return candidate
    return name


def _is_pg_or_pg_diploma(program_level, program_type):
    if (program_level or '').upper() == 'PG':
        return True
    p = (program_type or '').upper()
    if any(x in p for x in (
        'P. G. D. C. A', 'PGDCA', 'PG DIPLOMA', 'POST GRADUATE',
        'M.SC', 'M.A', 'M. A', 'M. SC', 'M.COM', 'M. COM', 'M.S.W', 'M. S. W'
    )):
        return True
    return False


def _get_program_courses(program_type):
    courses = ProgramCourse.objects.filter(program_type__iexact=program_type).order_by('sort_order', 'course_code')
    if not courses.exists():
        short_name = program_type.replace(' First Semester', '').strip()
        courses = ProgramCourse.objects.filter(program_type__iexact=short_name).order_by('sort_order', 'course_code')
    return courses


@student_login_required
@require_http_methods(['GET', 'POST'])
def enrollment_form(request):
    reg_no = request.session.get('reg_no')
    student = get_object_or_404(Student, registration_no=reg_no)
    existing_enrollment = StudentEnrollment.objects.filter(reg_no=reg_no).first()

    if request.method == 'GET' and existing_enrollment and existing_enrollment.is_submitted:
        if request.GET.get('edit') != '1':
            return redirect('enrollment_print', enrollment_no=existing_enrollment.enrollment_no)

    if request.method == 'POST':
        action = request.POST.get('action', 'submit')

        admission = StudentAdmission.objects.filter(reg_no=reg_no).order_by('-submitted_date', '-created_date').first()

        # Collect personal and contact data
        full_name = request.POST.get('full_name', '').strip() or student.full_name or (admission.full_name if admission else '') or ''
        father_name = request.POST.get('father_name', '').strip() or (admission.father_name if admission else '') or ''
        mother_name = request.POST.get('mother_name', '').strip() or (admission.mother_name if admission else '') or ''
        gender = request.POST.get('gender', '').strip() or (admission.gender if admission else '') or ''
        dob_str = request.POST.get('dob', '').strip() or (str(admission.dob) if admission and admission.dob else '')
        dob = dob_str if dob_str else None
        category = request.POST.get('category', '').strip() or (admission.category if admission else '') or ''
        nationality = request.POST.get('nationality', 'Indian').strip() or 'Indian'
        religion = request.POST.get('religion', '').strip() or (admission.religion if admission else '') or ''
        marital_status = request.POST.get('marital_status', '').strip() or (admission.marital_status if admission else '') or ''
        blood_group = request.POST.get('blood_group', '').strip() or (admission.blood_group if admission else '') or ''
        mobile = request.POST.get('mobile', '').strip() or student.mobile or (admission.mobile if admission else '') or ''
        email = request.POST.get('email', '').strip() or student.email or (admission.email if admission else '') or ''
        aadhaar = request.POST.get('aadhaar', '').strip() or student.aadhaar or (admission.aadhaar if admission else '') or ''
        apaar_id = request.POST.get('apaar_id', '').strip() or (admission.apaar_id if admission else '') or ''
        medium = request.POST.get('medium', '').strip() or (admission.medium if admission else '') or ''

        has_disability = request.POST.get('has_disability') in ('1', 'true', 'True', True)
        disability_details = request.POST.get('disability_details', '').strip()
        disability_percentage = request.POST.get('disability_percentage', '').strip()
        disability_type = request.POST.get('disability_type', '').strip()
        is_minority = request.POST.get('is_minority') in ('1', 'true', 'True', True)

        # Addresses
        perm_state = request.POST.get('perm_state', '').strip()
        perm_district = request.POST.get('perm_district', '').strip()
        perm_city = request.POST.get('perm_city', '').strip()
        perm_village = request.POST.get('perm_village', '').strip()
        perm_pin_code = request.POST.get('perm_pin_code', '').strip()

        corr_state = request.POST.get('corr_state', '').strip()
        corr_district = request.POST.get('corr_district', '').strip()
        corr_city = request.POST.get('corr_city', '').strip()
        corr_village = request.POST.get('corr_village', '').strip()
        corr_pin_code = request.POST.get('corr_pin_code', '').strip()

        # Education
        class10 = request.POST.get('class10', '10th').strip()
        board10 = request.POST.get('board10', '').strip()
        year10 = int(request.POST.get('year10')) if request.POST.get('year10') and request.POST.get('year10').isdigit() else None
        total_marks10 = request.POST.get('total_marks10', '').strip()
        obtained10 = request.POST.get('obtained10', '').strip()
        percentage10 = request.POST.get('percentage10', '').strip()
        grade10 = request.POST.get('grade10', '').strip()

        class12 = request.POST.get('class12', '12th').strip()
        board12 = request.POST.get('board12', '').strip()
        stream12 = request.POST.get('stream12', '').strip()
        year12 = int(request.POST.get('year12')) if request.POST.get('year12') and request.POST.get('year12').isdigit() else None
        total_marks12 = request.POST.get('total_marks12', '').strip()
        obtained12 = request.POST.get('obtained12', '').strip()
        percentage12 = request.POST.get('percentage12', '').strip()
        grade12 = request.POST.get('grade12', '').strip()

        class_grad = request.POST.get('class_grad', '').strip()
        board_grad = request.POST.get('board_grad', '').strip()
        stream_grad = request.POST.get('stream_grad', '').strip()
        year_grad = int(request.POST.get('year_grad')) if request.POST.get('year_grad') and request.POST.get('year_grad').isdigit() else None
        total_marks_grad = request.POST.get('total_marks_grad', '').strip()
        obtained_grad = request.POST.get('obtained_grad', '').strip()
        percentage_grad = request.POST.get('percentage_grad', '').strip()
        grade_grad = request.POST.get('grade_grad', '').strip()
        education_json = request.POST.get('education_json', '').strip() or None

        # Images
        photo_base64 = request.POST.get('photo_base64', '').strip()
        signature_base64 = request.POST.get('signature_base64', '').strip()

        # Payment details
        fee_amount = request.POST.get('fee_amount', '500').strip() or '500'
        transaction_id = request.POST.get('transaction_id', '').strip()
        payment_receipt_file = request.FILES.get('payment_receipt')
        payment_receipt_base64 = request.POST.get('payment_receipt_base64', '').strip()

        # Program & Courses - fixed as applied while admission time
        admission = StudentAdmission.objects.filter(reg_no=reg_no).order_by('-submitted_date', '-created_date').first()
        program_type = _normalize_program_name(request.POST.get('program_type', '').strip())
        if not program_type and admission and admission.program_type:
            program_type = _normalize_program_name(admission.program_type)
        if not program_type and student.program_type:
            program_type = _normalize_program_name(student.program_type)

        program_code = request.POST.get('program_code', '').strip()
        if not program_code and program_type:
            prog = Program.objects.filter(program_name__iexact=program_type).first()
            if not prog:
                short_name = program_type.replace(' First Semester', '').strip()
                prog = Program.objects.filter(program_name__iexact=short_name).first()
            if prog and prog.program_code:
                program_code = prog.program_code

        semester = request.POST.get('semester', 'I').strip() or 'I'
        bsc_subject_group = request.POST.get('bsc_subject_group', '').strip()
        selected_courses_json = request.POST.get('selected_courses_json', '').strip() or None

        if not selected_courses_json and existing_enrollment and existing_enrollment.selected_courses_json:
            selected_courses_json = existing_enrollment.selected_courses_json
        elif not selected_courses_json and admission and admission.selected_subjects_json:
            selected_courses_json = admission.selected_subjects_json

        if not bsc_subject_group and selected_courses_json:
            _, initial_group = parse_selected_subjects_payload(selected_courses_json)
            bsc_subject_group = initial_group

        if selected_courses_json and bsc_subject_group:
            try:
                parsed_c = json.loads(selected_courses_json)
                if isinstance(parsed_c, list):
                    selected_courses_json = json.dumps({
                        'bsc_subject_group': bsc_subject_group,
                        'courses': parsed_c,
                        'subjects': parsed_c,
                    })
            except Exception:
                pass

        enrollment = existing_enrollment or StudentEnrollment(student=student, reg_no=reg_no)
        enrollment.admission = admission
        enrollment.full_name = full_name
        enrollment.father_name = father_name
        enrollment.mother_name = mother_name
        enrollment.gender = gender
        enrollment.dob = dob
        enrollment.category = category
        enrollment.nationality = nationality
        enrollment.religion = religion
        enrollment.marital_status = marital_status
        enrollment.blood_group = blood_group
        enrollment.mobile = mobile
        enrollment.email = email
        enrollment.aadhaar = aadhaar
        enrollment.apaar_id = apaar_id
        enrollment.medium = medium
        enrollment.has_disability = has_disability
        enrollment.disability_details = disability_details
        enrollment.disability_percentage = disability_percentage
        enrollment.disability_type = disability_type
        enrollment.is_minority = is_minority

        enrollment.perm_state = perm_state
        enrollment.perm_district = perm_district
        enrollment.perm_city = perm_city
        enrollment.perm_village = perm_village
        enrollment.perm_pin_code = perm_pin_code

        enrollment.corr_state = corr_state
        enrollment.corr_district = corr_district
        enrollment.corr_city = corr_city
        enrollment.corr_village = corr_village
        enrollment.corr_pin_code = corr_pin_code

        enrollment.class10 = class10
        enrollment.board10 = board10
        enrollment.year10 = year10
        enrollment.total_marks10 = total_marks10
        enrollment.obtained10 = obtained10
        enrollment.percentage10 = percentage10
        enrollment.grade10 = grade10

        enrollment.class12 = class12
        enrollment.board12 = board12
        enrollment.stream12 = stream12
        enrollment.year12 = year12
        enrollment.total_marks12 = total_marks12
        enrollment.obtained12 = obtained12
        enrollment.percentage12 = percentage12
        enrollment.grade12 = grade12

        enrollment.class_grad = class_grad
        enrollment.board_grad = board_grad
        enrollment.stream_grad = stream_grad
        enrollment.year_grad = year_grad
        enrollment.total_marks_grad = total_marks_grad
        enrollment.obtained_grad = obtained_grad
        enrollment.percentage_grad = percentage_grad
        enrollment.grade_grad = grade_grad
        enrollment.education_json = education_json

        if photo_base64:
            enrollment.photo_base64 = photo_base64
        if signature_base64:
            enrollment.signature_base64 = signature_base64

        enrollment.program_type = program_type
        enrollment.program_code = program_code
        enrollment.semester = semester
        enrollment.selected_courses_json = selected_courses_json

        # Payment persistence
        enrollment.fee_amount = fee_amount
        if transaction_id:
            enrollment.transaction_id = transaction_id
            enrollment.payment_status = 'Paid'
        if payment_receipt_file:
            enrollment.payment_receipt = payment_receipt_file
        if payment_receipt_base64:
            enrollment.payment_receipt_base64 = payment_receipt_base64

        if action == 'save_payment':
            if not enrollment.transaction_id:
                messages.error(request, 'Please complete the ₹500 fee payment and enter your Transaction ID / UTR Number.')
                return redirect('enrollment_form')
            enrollment.status = 'Draft'
            enrollment.save()
            messages.success(request, 'Payment details submitted successfully! Section 3 and Course selection are now unlocked.')
            return redirect(reverse('enrollment_form') + '?step=section3')
        elif action == 'submit':
            if not enrollment.transaction_id:
                messages.error(request, 'Please complete the ₹500 fee payment and enter your Transaction ID / UTR Number before submitting.')
                return redirect('enrollment_form')
            if not enrollment.enrollment_no:
                enrollment.enrollment_no = generate_enrollment_number()
            enrollment.status = 'Submitted'
            enrollment.is_submitted = True
            enrollment.submitted_date = timezone.now()
            enrollment.save()
            messages.success(request, f'Enrollment application submitted successfully! Enrollment Number: {enrollment.enrollment_no}')
            return redirect('enrollment_print', enrollment_no=enrollment.enrollment_no)
        else:
            enrollment.status = 'Draft'
            enrollment.save()
            messages.info(request, 'Enrollment draft saved successfully.')
            return redirect('enrollment_form')

    # GET Request: Pre-populate
    admission = StudentAdmission.objects.filter(reg_no=reg_no).order_by('-submitted_date', '-created_date').first()

    initial_data = {}
    initial_bsc_group = ''
    if existing_enrollment:
        for f in [
            'full_name', 'father_name', 'mother_name', 'gender', 'dob', 'category', 'nationality',
            'religion', 'marital_status', 'blood_group', 'mobile', 'email', 'aadhaar', 'apaar_id',
            'medium', 'has_disability', 'disability_details', 'disability_percentage', 'disability_type',
            'is_minority', 'perm_state', 'perm_district', 'perm_city', 'perm_village', 'perm_pin_code',
            'corr_state', 'corr_district', 'corr_city', 'corr_village', 'corr_pin_code', 'class10',
            'board10', 'year10', 'total_marks10', 'obtained10', 'percentage10', 'grade10', 'class12',
            'board12', 'year12', 'total_marks12', 'obtained12', 'percentage12', 'grade12', 'stream12',
            'class_grad', 'board_grad', 'stream_grad', 'year_grad', 'total_marks_grad', 'obtained_grad',
            'percentage_grad', 'grade_grad',
            'photo_base64', 'signature_base64', 'program_type', 'program_code', 'semester', 'selected_courses_json',
            'fee_amount', 'payment_status', 'transaction_id', 'payment_receipt_base64'
        ]:
            val = getattr(existing_enrollment, f, None)
            initial_data[f] = val.isoformat() if hasattr(val, 'isoformat') else val
        if existing_enrollment.payment_receipt:
            try:
                initial_data['payment_receipt_url'] = existing_enrollment.payment_receipt.url
            except Exception:
                pass
    elif admission:
        for f in [
            'full_name', 'father_name', 'mother_name', 'gender', 'dob', 'category', 'nationality',
            'religion', 'marital_status', 'blood_group', 'mobile', 'email', 'aadhaar', 'apaar_id',
            'medium', 'has_disability', 'disability_details', 'disability_percentage', 'disability_type',
            'is_minority', 'perm_state', 'perm_district', 'perm_city', 'perm_village', 'perm_pin_code',
            'corr_state', 'corr_district', 'corr_city', 'corr_village', 'corr_pin_code', 'class10',
            'board10', 'year10', 'total_marks10', 'obtained10', 'percentage10', 'grade10', 'class12',
            'board12', 'year12', 'total_marks12', 'obtained12', 'percentage12', 'grade12', 'stream12',
            'class_grad', 'board_grad', 'stream_grad', 'year_grad', 'total_marks_grad', 'obtained_grad',
            'percentage_grad', 'grade_grad',
            'photo_base64', 'signature_base64', 'program_type', 'selected_subjects_json'
        ]:
            val = getattr(admission, f, None)
            initial_data[f] = val.isoformat() if hasattr(val, 'isoformat') else val
        initial_data['selected_courses_json'] = admission.selected_subjects_json
        initial_data['semester'] = 'I'
        initial_data['fee_amount'] = '500'
        initial_data['payment_status'] = 'Pending'
        initial_data['transaction_id'] = ''
        initial_data['payment_receipt_url'] = ''
        initial_data['payment_receipt_base64'] = ''
    else:
        initial_data = {
            'full_name': student.full_name,
            'mobile': student.mobile,
            'email': student.email,
            'aadhaar': student.aadhaar,
            'program_type': student.program_type or 'B.A. First Semester',
            'semester': 'I',
        }

    # Ensure graduation and 10th details are populated from build_education_list if not already in initial_data
    if admission:
        for edu in build_education_list(admission):
            if edu.get('RowKey') == 'grad' and not initial_data.get('class_grad') and not initial_data.get('board_grad'):
                initial_data['class_grad'] = edu.get('ClassName') or ''
                initial_data['board_grad'] = edu.get('Board') or ''
                initial_data['stream_grad'] = edu.get('Stream') or ''
                initial_data['year_grad'] = edu.get('Year') or ''
                initial_data['total_marks_grad'] = edu.get('TotalMarks') or ''
                initial_data['obtained_grad'] = edu.get('Obtained') or ''
                initial_data['percentage_grad'] = edu.get('Percentage') or ''
                initial_data['grade_grad'] = edu.get('Grade') or ''
            elif edu.get('RowKey') == '10' and not initial_data.get('board10'):
                initial_data['board10'] = edu.get('Board') or ''
                initial_data['year10'] = edu.get('Year') or ''
                initial_data['total_marks10'] = edu.get('TotalMarks') or ''
                initial_data['obtained10'] = edu.get('Obtained') or ''
                initial_data['percentage10'] = edu.get('Percentage') or ''
                initial_data['grade10'] = edu.get('Grade') or ''

    program_types = get_program_names()
    programs_by_level = get_programs_by_level()

    initial_program = _normalize_program_name(
        initial_data.get('program_type') or (admission.program_type if admission else '') or student.program_type or 'B.A. First Semester'
    )
    selected_program_type = normalize_program_type_for_display(initial_program, program_types)
    selected_program_level = get_program_level_for_name(selected_program_type)

    initial_data['program_type'] = selected_program_type
    initial_data['program_level'] = selected_program_level

    show_ug_qualification = _is_pg_or_pg_diploma(selected_program_level, selected_program_type)

    # Parse initial selected courses and bsc group
    initial_courses_list = []
    raw_courses = initial_data.get('selected_courses_json')
    if raw_courses:
        initial_courses_list, initial_bsc_group = parse_selected_subjects_payload(raw_courses)
        if not initial_courses_list and isinstance(raw_courses, str):
            try:
                parsed = json.loads(raw_courses)
                if isinstance(parsed, list):
                    initial_courses_list = parsed
                elif isinstance(parsed, dict):
                    initial_courses_list = parsed.get('courses') or parsed.get('subjects') or []
                    initial_bsc_group = parsed.get('bsc_subject_group') or initial_bsc_group
            except Exception:
                initial_courses_list = []

    bsc_subject_groups = get_bsc_subject_group_sections(selected_program_type)
    bsc_program_name = BSC_PROGRAM
    bsc_program_names = [pt for pt in program_types if is_bsc_program(pt)]

    program_level_choices = [
        {'value': level, 'label': PROGRAM_LEVEL_DISPLAY[level]}
        for level in PROGRAM_LEVEL_CHOICES
        if programs_by_level.get(level)
    ]

    is_payment_done = bool(existing_enrollment and existing_enrollment.transaction_id)
    active_step = request.GET.get('step', '')

    ctx = {
        'student': student,
        'admission': admission,
        'existing_enrollment': existing_enrollment,
        'initial_data': initial_data,
        'is_payment_done': is_payment_done,
        'active_step': active_step,
        'show_ug_qualification': show_ug_qualification,
        'program_types': program_types,
        'selected_program_type': selected_program_type,
        'selected_program_level': selected_program_level,
        'programs_by_level': programs_by_level,
        'programs_by_level_json': json.dumps(programs_by_level),
        'program_level_choices': program_level_choices,
        'bsc_subject_groups': bsc_subject_groups,
        'bsc_program_name': bsc_program_name,
        'bsc_program_names_json': json.dumps(bsc_program_names),
        'initial_program_type': selected_program_type,
        'initial_program_level': selected_program_level,
        'initial_bsc_group': initial_bsc_group,
        'initial_courses_data': initial_courses_list,
        'religion_choices': RELIGION_CHOICES,
        'medium_choices': MEDIUM_CHOICES,
    }
    ctx.update(get_student_sidebar_context(reg_no, active='enrollment'))
    return render(request, 'admissions/enrollment_form.html', ctx)


def enrollment_print(request, enrollment_no=None):
    admin_user = request.session.get('admin_user')
    reg_no = request.session.get('reg_no')
    if not reg_no and not admin_user:
        return redirect('login')

    enrollment = None
    if enrollment_no:
        if str(enrollment_no).isdigit():
            enrollment = StudentEnrollment.objects.filter(
                models.Q(enrollment_no=enrollment_no) | models.Q(pk=int(enrollment_no))
            ).first()
        else:
            enrollment = StudentEnrollment.objects.filter(enrollment_no=enrollment_no).first()

    if admin_user:
        if not enrollment:
            if enrollment_no:
                enrollment = get_object_or_404(StudentEnrollment, enrollment_no=enrollment_no)
            elif reg_no:
                enrollment = StudentEnrollment.objects.filter(reg_no=reg_no, is_submitted=True).order_by('-submitted_date').first()
                if not enrollment:
                    enrollment = get_object_or_404(StudentEnrollment, reg_no=reg_no)
            else:
                messages.error(request, 'Enrollment record not found.')
                return redirect('admin_dashboard')
        student = enrollment.student
    else:
        student = get_object_or_404(Student, registration_no=reg_no)
        if not enrollment:
            if enrollment_no:
                enrollment = get_object_or_404(StudentEnrollment, enrollment_no=enrollment_no, reg_no=reg_no)
            else:
                enrollment = StudentEnrollment.objects.filter(reg_no=reg_no, is_submitted=True).order_by('-submitted_date').first()
                if not enrollment:
                    messages.warning(request, 'No submitted enrollment application found. Please complete enrollment first.')
                    return redirect('enrollment_form')
        elif enrollment.reg_no != reg_no:
            raise Http404("No StudentEnrollment matches the given query.")

    if not enrollment.enrollment_no:
        from .utils import generate_enrollment_number
        enrollment.enrollment_no = generate_enrollment_number()
        enrollment.save(update_fields=['enrollment_no'])

    enrolled_courses = []
    if enrollment.selected_courses_json:
        try:
            raw_courses, bsc_group = parse_selected_subjects_payload(enrollment.selected_courses_json)
            if not raw_courses and isinstance(enrollment.selected_courses_json, str):
                parsed = json.loads(enrollment.selected_courses_json)
                if isinstance(parsed, list):
                    raw_courses = parsed
                elif isinstance(parsed, dict):
                    raw_courses = parsed.get('courses') or parsed.get('subjects') or []

            for c in raw_courses:
                if isinstance(c, dict):
                    name = c.get('name') or c.get('course_name') or ''
                    code = c.get('code') or c.get('course_code') or ''
                    paper = c.get('paper') or c.get('paper_no') or ''
                    type_1 = c.get('type_1') or c.get('type1') or c.get('course_type_1') or ''
                    type_2 = c.get('type_2') or c.get('type2') or c.get('course_type_2') or ''
                    dept = c.get('dept') or c.get('department') or ''

                    # If code or paper is missing, lookup in ProgramCourse
                    if (not code or not paper or not type_1 or not type_2) and name:
                        clean_name = name.split('—')[-1].strip() if '—' in name else name
                        db_course = ProgramCourse.objects.filter(
                            program_type__iexact=enrollment.program_type
                        ).filter(
                            models.Q(course_name__iexact=name) | models.Q(course_name__iexact=clean_name)
                        ).first()
                        if not db_course:
                            short_program = enrollment.program_type.replace(' First Semester', '').strip()
                            db_course = ProgramCourse.objects.filter(
                                program_type__iexact=short_program
                            ).filter(
                                models.Q(course_name__iexact=name) | models.Q(course_name__iexact=clean_name)
                            ).first()
                        if not db_course and dept:
                            db_course = ProgramCourse.objects.filter(
                                program_type__iexact=enrollment.program_type,
                                department__iexact=dept,
                            ).filter(
                                models.Q(course_type_2__iexact=type_2) if type_2 else models.Q()
                            ).first()
                            if not db_course:
                                short_program = enrollment.program_type.replace(' First Semester', '').strip()
                                db_course = ProgramCourse.objects.filter(
                                    program_type__iexact=short_program,
                                    department__iexact=dept,
                                ).filter(
                                    models.Q(course_type_2__iexact=type_2) if type_2 else models.Q()
                                ).first()
                        if db_course:
                            code = code or db_course.course_code
                            paper = paper or db_course.paper_no
                            type_1 = type_1 or db_course.course_type_1
                            type_2 = type_2 or db_course.course_type_2
                            dept = dept or db_course.department

                    # Default paper number to 'I' if blank or '-'
                    paper_str = str(paper).strip() if paper else ''
                    if not paper_str or paper_str == '-':
                        paper_str = 'I'

                    enrolled_courses.append({
                        'code': code or '-',
                        'name': name,
                        'paper': paper_str,
                        'type_1': type_1 or 'Theory',
                        'type_2': type_2 or 'DSC',
                        'dept': dept,
                    })
        except Exception as e:
            logger.error(f'Error parsing enrolled courses: {e}')
            enrolled_courses = []

    ctx = {
        'student': student,
        'enrollment': enrollment,
        'enrolled_courses': enrolled_courses,
    }
    if reg_no and not admin_user:
        ctx.update(get_student_sidebar_context(reg_no, active='enrollment'))
    return render(request, 'admissions/enrollment_print.html', ctx)


def enrollment_fee_receipt(request, enrollment_no=None):
    admin_user = request.session.get('admin_user')
    reg_no = request.session.get('reg_no')
    if not reg_no and not admin_user:
        return redirect('login')

    enrollment = None
    if enrollment_no:
        if str(enrollment_no).isdigit():
            enrollment = StudentEnrollment.objects.filter(
                models.Q(enrollment_no=enrollment_no) | models.Q(pk=int(enrollment_no))
            ).first()
        else:
            enrollment = StudentEnrollment.objects.filter(enrollment_no=enrollment_no).first()

    if admin_user:
        if not enrollment:
            if enrollment_no:
                enrollment = get_object_or_404(StudentEnrollment, enrollment_no=enrollment_no)
            elif reg_no:
                enrollment = StudentEnrollment.objects.filter(reg_no=reg_no, is_submitted=True).order_by('-submitted_date').first()
                if not enrollment:
                    enrollment = get_object_or_404(StudentEnrollment, reg_no=reg_no)
            else:
                messages.error(request, 'Enrollment record not found.')
                return redirect('admin_dashboard')
        student = enrollment.student
    else:
        student = get_object_or_404(Student, registration_no=reg_no)
        if not enrollment:
            if enrollment_no:
                enrollment = get_object_or_404(StudentEnrollment, enrollment_no=enrollment_no, reg_no=reg_no)
            else:
                enrollment = StudentEnrollment.objects.filter(reg_no=reg_no, is_submitted=True).order_by('-submitted_date').first()
                if not enrollment:
                    messages.warning(request, 'No submitted enrollment application found. Please complete enrollment first.')
                    return redirect('enrollment_form')
        elif enrollment.reg_no != reg_no:
            raise Http404("No StudentEnrollment matches the given query.")

    # Prepare program display with code
    program_code = enrollment.program_code or ''
    if not program_code and enrollment.program_type:
        prog = Program.objects.filter(program_name__iexact=enrollment.program_type).first()
        if prog and prog.program_code:
            program_code = prog.program_code
        else:
            short_p = enrollment.program_type.replace(' First Semester', '').strip()
            prog = Program.objects.filter(program_name__iexact=short_p).first()
            if prog and prog.program_code:
                program_code = prog.program_code

    program_display = enrollment.program_type.upper() if enrollment.program_type else ''
    if program_code:
        program_display = f"{program_code}-{program_display}"

    sub_date = enrollment.submitted_date or timezone.now()
    deposit_date = sub_date.strftime('%d/%m/%Y at %I:%M %p')
    month_year = sub_date.strftime('%b. / %Y').upper()

    ctx = {
        'student': student,
        'enrollment': enrollment,
        'program_display': program_display,
        'deposit_date': deposit_date,
        'month_year': month_year,
        'fee_amount': enrollment.fee_amount or '500',
        'transaction_id': enrollment.transaction_id or '',
        'payment_status': enrollment.payment_status or ('Paid' if enrollment.transaction_id else 'Pending'),
    }
    return render(request, 'admissions/enrollment_receipt.html', ctx)


@student_login_required
@require_http_methods(['POST'])
def cancel_enrollment(request):
    reg_no = request.session.get('reg_no')
    enrollment = StudentEnrollment.objects.filter(reg_no=reg_no).order_by('-submitted_date', '-created_at').first()
    if not enrollment:
        messages.error(request, 'No enrollment application found to cancel.')
        return redirect('student_dashboard')

    if enrollment.status == 'Approved':
        messages.error(
            request,
            'Cannot cancel enrollment. Your enrollment application has already been accepted/approved by the admin.'
        )
        return redirect('student_dashboard')

    enrollment.status = 'Draft'
    enrollment.is_submitted = False
    enrollment.save(update_fields=['status', 'is_submitted', 'updated_at'])

    messages.success(
        request,
        'Enrollment application cancelled successfully. You can now edit any incorrect entries and re-submit your form.'
    )
    return redirect('enrollment_form')


