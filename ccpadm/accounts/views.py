import json
import re
from datetime import datetime, timedelta

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from admissions.models import StudentAdmission, StudentEnrollment
from courses.constants import PROGRAM_LEVEL_CHOICES
from courses.utils import get_programs_by_level

from .forms import HelpdeskIssueForm
from .models import HelpdeskOfficer, HelpdeskIssue, ImportantInstruction, Notice, PasswordResetOTP, Student
from .utils import (
    admin_login_required,
    generate_otp,
    generate_registration_no,
    generate_secure_password,
    hash_otp,
    is_valid_aadhaar,
    is_valid_email,
    is_valid_mobile,
    mask_aadhaar,
    send_otp_email,
    send_registration_email,
    student_login_required,
)


def _home_page_context():
    now = timezone.now()
    return {
        'important_instructions': ImportantInstruction.objects.filter(is_active=True).order_by(
            'sort_order', '-created_at'
        ),
        'notices': Notice.objects.filter(
            is_active=True,
        ).filter(
            Q(expires_at__isnull=True) | Q(expires_at__gt=now),
        ).order_by('sort_order', '-created_at'),
    }


def home(request):
    return render(request, 'home.html', _home_page_context())


@require_http_methods(['GET', 'POST'])
def helpdesk(request):
    officers = HelpdeskOfficer.objects.filter(is_active=True).order_by('sort_order', 'name')
    initial = {}
    if request.session.get('is_logged_in'):
        initial = {
            'name': request.session.get('student_name', ''),
            'email': request.session.get('student_email', ''),
            'mobile': request.session.get('student_mobile', ''),
            'registration_no': request.session.get('reg_no', ''),
        }

    if request.method == 'POST':
        form = HelpdeskIssueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Your issue has been submitted successfully. Our helpdesk team will contact you soon.',
            )
            return redirect('helpdesk')
    else:
        form = HelpdeskIssueForm(initial=initial)

    return render(request, 'accounts/helpdesk.html', {
        'officers': officers,
        'form': form,
    })


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.session.get('is_logged_in'):
        return redirect('student_dashboard')
    if request.method == 'POST':
        user_input = request.POST.get('user', '').strip()
        password = request.POST.get('password', '').strip()
        if not user_input or not password:
            messages.error(request, 'Please enter both Email/Mobile and Password.')
        else:
            student = Student.objects.filter(
                Q(email__iexact=user_input) | Q(mobile=user_input),
                password=password,
            ).first()
            if student:
                request.session['is_logged_in'] = True
                request.session['reg_no'] = student.registration_no
                request.session['student_name'] = student.full_name
                request.session['student_email'] = student.email
                request.session['student_mobile'] = student.mobile
                return redirect('student_dashboard')
            messages.error(request, 'Invalid login credentials.')
    return render(request, 'accounts/login.html')


def logout_view(request):
    request.session.flush()
    return redirect('home')


REGISTRATION_PROGRAM_LEVEL_LABELS = {
    'UG': 'Under Graduate',
    'PG': 'Post Graduate',
    'Diploma': 'Diploma',
}


@require_http_methods(['GET', 'POST'])
def registration_view(request):
    programs_by_level = get_programs_by_level()
    program_level_choices = [
        {
            'value': level,
            'label': REGISTRATION_PROGRAM_LEVEL_LABELS.get(level, level),
        }
        for level in PROGRAM_LEVEL_CHOICES
    ]

    success_data = None
    selected_program_level = ''
    selected_program_name = ''

    if request.GET.get('success') and request.session.get('registration_no'):
        success_data = {
            'reg_no': request.session.pop('registration_no', ''),
            'password': request.session.pop('temp_password', ''),
        }

    if request.method == 'POST':
        first = request.POST.get('first_name', '').strip()
        middle = request.POST.get('middle_name', '').strip()
        last = request.POST.get('last_name', '').strip()
        full_name = ' '.join(p for p in [first, middle, last] if p)
        email = request.POST.get('email', '').strip().lower()
        mobile = re.sub(r'\D', '', request.POST.get('mobile', '').strip())
        aadhaar = re.sub(r'\D', '', request.POST.get('aadhaar', '').strip())
        selected_program_level = request.POST.get('program_level', '').strip()
        selected_program_name = request.POST.get('program_name', '').strip()
        program_type = selected_program_name

        errors = []
        if not selected_program_level:
            errors.append('Please select Program Type.')
        elif selected_program_level not in PROGRAM_LEVEL_CHOICES:
            errors.append('Invalid Program Type selected.')
        if not selected_program_name:
            errors.append('Please select Program Name.')
        elif selected_program_name not in programs_by_level.get(selected_program_level, []):
            errors.append('Selected Program Name does not match the chosen Program Type.')
        if not full_name:
            errors.append('Name is required.')
        if not is_valid_email(email):
            errors.append('Invalid Email format.')
        if not is_valid_mobile(mobile):
            errors.append('Invalid Mobile Number. Must be 10 digits starting with 6-9.')
        if not is_valid_aadhaar(aadhaar):
            errors.append('Invalid Aadhaar Number. Must be exactly 12 digits.')

        if errors:
            for e in errors:
                messages.error(request, e)
        else:
            exists = Student.objects.filter(
                Q(email__iexact=email) | Q(mobile=mobile) | Q(aadhaar=aadhaar)
            ).exists()
            if exists:
                messages.error(request, 'Already registered with this Email, Mobile, or Aadhaar.')
            else:
                password = generate_secure_password()
                reg_no = generate_registration_no(program_type)
                Student.objects.create(
                    registration_no=reg_no,
                    full_name=full_name,
                    email=email,
                    mobile=mobile,
                    password=password,
                    aadhaar=aadhaar,
                    program_type=program_type,
                    created_date=timezone.now(),
                )
                send_registration_email(email, full_name, reg_no, password)
                request.session['registration_no'] = reg_no
                request.session['temp_password'] = password
                return redirect('/register/?success=1')

    return render(request, 'accounts/registration.html', {
        'program_level_choices': program_level_choices,
        'programs_by_level_json': json.dumps(programs_by_level),
        'selected_program_level': selected_program_level,
        'selected_program_name': selected_program_name,
        'success_data': success_data,
    })


@student_login_required
def student_dashboard(request):
    reg_no = request.session.get('reg_no')
    student = Student.objects.filter(registration_no=reg_no).first()
    if not student:
        messages.error(request, 'Student record not found.')
        return redirect('login')

    from admissions.services import (
        get_editable_admission,
        get_printable_admission,
        get_program_display_name,
        parse_selected_subjects,
    )

    admission = get_printable_admission(reg_no) or get_editable_admission(reg_no)
    selected_subjects = parse_selected_subjects(admission) if admission else []
    program_display = ''
    if admission and admission.program_type:
        program_display = get_program_display_name(admission)
    elif student.program_type:
        program_display = student.program_type
    else:
        program_display = 'Not Selected'

    courses_display = ''
    if admission and admission.subject:
        courses_display = admission.subject
    elif selected_subjects:
        courses_display = ', '.join(
            s.get('name', '') for s in selected_subjects if isinstance(s, dict) and s.get('name')
        )

    from admissions.models import StudentEnrollment, EnrollmentInstruction
    from .utils import get_student_sidebar_context

    enrollment = StudentEnrollment.objects.filter(reg_no=reg_no).order_by('-submitted_date', '-created_at').first()
    can_cancel_enrollment = bool(enrollment and enrollment.is_submitted and enrollment.status != 'Approved')
    enrollment_instruction = EnrollmentInstruction.objects.filter(is_active=True).first()

    ctx = {
        'student': student,
        'admission': admission,
        'enrollment': enrollment,
        'enrollment_instruction': enrollment_instruction,
        'can_cancel_enrollment': can_cancel_enrollment,
        'masked_aadhaar': mask_aadhaar(student.aadhaar),
        'program_display': program_display,
        'selected_subjects': selected_subjects,
        'courses_display': courses_display,
    }
    ctx.update(get_student_sidebar_context(reg_no, active='dashboard'))
    return render(request, 'accounts/student_dashboard.html', ctx)


def _parse_recovery_dob(dob_str):
    if not dob_str:
        return None
    dob_str = str(dob_str).strip()
    for fmt in ('%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y', '%Y/%m/%d'):
        try:
            return datetime.strptime(dob_str, fmt).date()
        except ValueError:
            pass
    return None


def _match_student_name(full_name_input, candidate_name):
    if not full_name_input or not candidate_name:
        return False
    clean_input = ' '.join(str(full_name_input).strip().lower().split())
    clean_candidate = ' '.join(str(candidate_name).strip().lower().split())
    if not clean_input or not clean_candidate:
        return False

    # Exact normalized match
    if clean_input == clean_candidate:
        return True

    input_tokens = clean_input.split()
    cand_tokens = clean_candidate.split()

    # Same set of tokens in any order (e.g., "Kumar Amar" vs "Amar Kumar")
    if set(input_tokens) == set(cand_tokens):
        return True

    # All tokens of input are in candidate (e.g. entered "Sonam Barman" for "Sonam Singh Barman")
    if all(tok in cand_tokens for tok in input_tokens):
        return True

    # All tokens of candidate in input (e.g. entered extra middle name or title)
    if all(tok in input_tokens for tok in cand_tokens):
        return True

    # Compact match ignoring whitespace (for compound names like Devid Gayakwad vs Devid Gayak Wad)
    if clean_input.replace(' ', '') == clean_candidate.replace(' ', ''):
        return True

    return False


def find_student_for_password_recovery(full_name, dob, aadhaar_input):
    """
    Validates full name, DOB, and Aadhaar to find matching student and their password.
    Returns (student, error_message).
    """
    clean_name = (full_name or '').strip()
    clean_aadhaar = re.sub(r'\D', '', aadhaar_input or '')

    if not clean_name:
        return None, 'Please enter your Full Name.'
    if not dob:
        return None, 'Please enter a valid Date of Birth.'
    if not clean_aadhaar or len(clean_aadhaar) != 12:
        return None, 'Please enter a valid 12-digit Aadhaar Number.'

    # Find candidates by Aadhaar across Student, StudentAdmission, and StudentEnrollment
    students_by_aadhaar = list(Student.objects.filter(aadhaar=clean_aadhaar))
    adm_by_aadhaar = list(StudentAdmission.objects.filter(aadhaar=clean_aadhaar))
    enr_by_aadhaar = list(StudentEnrollment.objects.filter(aadhaar=clean_aadhaar))

    candidate_reg_nos = set()
    for s in students_by_aadhaar:
        candidate_reg_nos.add(s.registration_no)
    for a in adm_by_aadhaar:
        if a.reg_no:
            candidate_reg_nos.add(a.reg_no)
    for e in enr_by_aadhaar:
        if e.reg_no:
            candidate_reg_nos.add(e.reg_no)

    if not candidate_reg_nos:
        # Check if Aadhaar was recorded with spaces or formatting in legacy records
        for s in Student.objects.filter(aadhaar__icontains=clean_aadhaar[-8:]):
            s_aadhaar_clean = re.sub(r'\D', '', s.aadhaar or '')
            if s_aadhaar_clean == clean_aadhaar:
                candidate_reg_nos.add(s.registration_no)

    if not candidate_reg_nos:
        return None, 'No student record found matching the provided Aadhaar Number.'

    matched_student = None
    for reg_no in candidate_reg_nos:
        student = Student.objects.filter(registration_no=reg_no).first()
        if not student:
            continue

        adm = StudentAdmission.objects.filter(reg_no=reg_no).first()
        enr = StudentEnrollment.objects.filter(reg_no=reg_no).first()

        # Check DOB
        candidate_dobs = [d for d in [getattr(adm, 'dob', None), getattr(enr, 'dob', None)] if d]
        for a in adm_by_aadhaar:
            if a.dob and a.dob not in candidate_dobs:
                candidate_dobs.append(a.dob)
        for e in enr_by_aadhaar:
            if e.dob and e.dob not in candidate_dobs:
                candidate_dobs.append(e.dob)

        if dob not in candidate_dobs:
            continue

        # Check Name
        name_candidates = [student.full_name]
        if adm and adm.full_name:
            name_candidates.append(adm.full_name)
        if enr and enr.full_name:
            name_candidates.append(enr.full_name)

        if any(_match_student_name(clean_name, name) for name in name_candidates):
            matched_student = student
            break

    if not matched_student:
        return None, (
            'The details provided do not match our records. '
            'Please verify your Full Name, Date of Birth, and Aadhaar Number.'
        )

    return matched_student, None


@require_http_methods(['GET', 'POST'])
def forgot_password(request):
    success = False
    matched_student = None
    error_message = None
    form_data = {
        'full_name': '',
        'dob': '',
        'aadhaar': '',
    }

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        dob_str = request.POST.get('dob', '').strip()
        aadhaar = request.POST.get('aadhaar', '').strip()

        form_data = {
            'full_name': full_name,
            'dob': dob_str,
            'aadhaar': aadhaar,
        }

        parsed_dob = _parse_recovery_dob(dob_str)
        matched_student, error_message = find_student_for_password_recovery(
            full_name=full_name,
            dob=parsed_dob,
            aadhaar_input=aadhaar,
        )

        if matched_student:
            success = True
            messages.success(request, 'Student identity verified successfully!')
        else:
            messages.error(request, error_message)

    return render(request, 'accounts/forgot_password.html', {
        'success': success,
        'matched_student': matched_student,
        'error_message': error_message,
        'form_data': form_data,
    })