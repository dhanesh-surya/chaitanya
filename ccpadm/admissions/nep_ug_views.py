import base64
import json
import logging
from datetime import datetime

from django.db import models
from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from accounts.models import Student
from accounts.utils import get_student_sidebar_context, student_login_required
from admissions.constants import MEDIUM_CHOICES, RELIGION_CHOICES
from admissions.models import NepUgAdmissionEnrollment, StudentAdmission, StudentEnrollment
from admissions.services import build_education_list
from admissions.utils import generate_enrollment_number

logger = logging.getLogger(__name__)

NEP_UG_PROGRAM_CHOICES = [
    ('B.A.', 'Bachelor of Arts (B.A.)'),
    ('B.Sc. Bio Group', 'Bachelor of Science - Biology Group (B.Sc. Bio)'),
    ('B.Sc. Maths Group', 'Bachelor of Science - Mathematics Group (B.Sc. Maths)'),
    ('B.Sc. Computer Science', 'Bachelor of Science - Computer Science (B.Sc. CS)'),
    ('B.Com', 'Bachelor of Commerce (B.Com)'),
    ('BCA', 'Bachelor of Computer Applications (BCA)'),
    ('BBA', 'Bachelor of Business Administration (BBA)'),
]


def generate_nep_ug_application_number():
    date_part = timezone.now().strftime('%d%m%y')
    prefix = f'NEP{date_part}'
    last = (
        NepUgAdmissionEnrollment.objects.filter(application_no__startswith=prefix)
        .order_by('-application_no')
        .values_list('application_no', flat=True)
        .first()
    )
    if last and len(last) >= 13:
        try:
            seq = int(last[-4:]) + 1
        except ValueError:
            seq = 1
    else:
        seq = 1
    return f'{prefix}{seq:04d}'


def _clean_ug_program_name(name):
    """Normalize program name down to base NEP UG program name."""
    if not name:
        return 'B.A.'
    n = name.replace(' First Semester', '').replace(' 1st Semester', '').strip()
    if 'B.SC' in n.upper() or 'BSC' in n.upper():
        if 'BIO' in n.upper():
            return 'B.Sc. Bio Group'
        if 'MATH' in n.upper():
            return 'B.Sc. Maths Group'
        if 'COMP' in n.upper() or 'CS' in n.upper():
            return 'B.Sc. Computer Science'
        return 'B.Sc. Bio Group'
    if 'B.COM' in n.upper() or 'BCOM' in n.upper():
        return 'B.Com'
    if 'BCA' in n.upper():
        return 'BCA'
    if 'BBA' in n.upper():
        return 'BBA'
    if 'B.A' in n.upper() or 'BA' in n.upper():
        return 'B.A.'
    return n


@student_login_required
@require_http_methods(['GET', 'POST'])
def nep_ug_enrollment_form(request):
    reg_no = request.session.get('reg_no')
    student = get_object_or_404(Student, registration_no=reg_no)
    existing_nep = NepUgAdmissionEnrollment.objects.filter(reg_no=reg_no).first()

    if request.method == 'GET' and existing_nep and existing_nep.is_submitted:
        if request.GET.get('edit') != '1':
            return redirect('nep_ug_print', enrollment_no=existing_nep.enrollment_no or existing_nep.application_no)

    admission = StudentAdmission.objects.filter(reg_no=reg_no).order_by('-submitted_date', '-created_date').first()
    first_sem_enrollment = StudentEnrollment.objects.filter(reg_no=reg_no).order_by('-submitted_date', '-created_at').first()

    if request.method == 'POST':
        action = request.POST.get('action', 'submit')

        # Program & Semester Info
        program_type = request.POST.get('program_type', '').strip() or 'B.A.'
        program_code = request.POST.get('program_code', '').strip()
        semester = request.POST.get('semester', 'II').strip() or 'II'
        academic_session = request.POST.get('academic_session', '2026-27').strip() or '2026-27'
        previous_roll_no = request.POST.get('previous_roll_no', '').strip()
        previous_enrollment_no = request.POST.get('previous_enrollment_no', '').strip()
        previous_semester_result = request.POST.get('previous_semester_result', 'Pass').strip() or 'Pass'
        previous_semester_marks = request.POST.get('previous_semester_marks', '').strip()

        # Personal and contact data
        full_name = request.POST.get('full_name', '').strip() or student.full_name or (admission.full_name if admission else '')
        father_name = request.POST.get('father_name', '').strip() or (admission.father_name if admission else '')
        mother_name = request.POST.get('mother_name', '').strip() or (admission.mother_name if admission else '')
        gender = request.POST.get('gender', '').strip() or (admission.gender if admission else '')
        dob_str = request.POST.get('dob', '').strip() or (str(admission.dob) if admission and admission.dob else '')
        dob = None
        if dob_str:
            for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y'):
                try:
                    dob = datetime.strptime(dob_str, fmt).date()
                    break
                except ValueError:
                    pass

        category = request.POST.get('category', '').strip() or (admission.category if admission else '')
        nationality = request.POST.get('nationality', 'Indian').strip() or 'Indian'
        religion = request.POST.get('religion', '').strip() or (admission.religion if admission else '')
        marital_status = request.POST.get('marital_status', '').strip() or (admission.marital_status if admission else '')
        blood_group = request.POST.get('blood_group', '').strip() or (admission.blood_group if admission else '')
        mobile = request.POST.get('mobile', '').strip() or student.mobile or (admission.mobile if admission else '')
        email = request.POST.get('email', '').strip() or student.email or (admission.email if admission else '')
        aadhaar = request.POST.get('aadhaar', '').strip() or student.aadhaar or (admission.aadhaar if admission else '')
        apaar_id = request.POST.get('apaar_id', '').strip() or (admission.apaar_id if admission else '')
        medium = request.POST.get('medium', '').strip() or (admission.medium if admission else '')

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

        # Photos & Signatures
        photo_base64 = request.POST.get('photo_base64', '').strip()
        signature_base64 = request.POST.get('signature_base64', '').strip()

        # Payment details
        fee_amount = request.POST.get('fee_amount', '500').strip() or '500'
        transaction_id = request.POST.get('transaction_id', '').strip()
        payment_receipt_file = request.FILES.get('payment_receipt')
        payment_receipt_base64 = request.POST.get('payment_receipt_base64', '').strip()

        # Subjects note / future JSON
        selected_courses_json = request.POST.get('selected_courses_json', '').strip() or None

        nep_record = existing_nep or NepUgAdmissionEnrollment(student=student, reg_no=reg_no)
        nep_record.admission = admission
        nep_record.first_sem_enrollment = first_sem_enrollment

        nep_record.program_type = program_type
        nep_record.program_code = program_code
        nep_record.semester = semester
        nep_record.academic_session = academic_session
        nep_record.previous_roll_no = previous_roll_no
        nep_record.previous_enrollment_no = previous_enrollment_no
        nep_record.previous_semester_result = previous_semester_result
        nep_record.previous_semester_marks = previous_semester_marks

        nep_record.full_name = full_name
        nep_record.father_name = father_name
        nep_record.mother_name = mother_name
        nep_record.gender = gender
        nep_record.dob = dob
        nep_record.category = category
        nep_record.nationality = nationality
        nep_record.religion = religion
        nep_record.marital_status = marital_status
        nep_record.blood_group = blood_group
        nep_record.mobile = mobile
        nep_record.email = email
        nep_record.aadhaar = aadhaar
        nep_record.apaar_id = apaar_id
        nep_record.medium = medium

        nep_record.has_disability = has_disability
        nep_record.disability_details = disability_details
        nep_record.disability_percentage = disability_percentage
        nep_record.disability_type = disability_type
        nep_record.is_minority = is_minority

        nep_record.perm_state = perm_state
        nep_record.perm_district = perm_district
        nep_record.perm_city = perm_city
        nep_record.perm_village = perm_village
        nep_record.perm_pin_code = perm_pin_code

        nep_record.corr_state = corr_state
        nep_record.corr_district = corr_district
        nep_record.corr_city = corr_city
        nep_record.corr_village = corr_village
        nep_record.corr_pin_code = corr_pin_code

        nep_record.class10 = class10
        nep_record.board10 = board10
        nep_record.year10 = year10
        nep_record.total_marks10 = total_marks10
        nep_record.obtained10 = obtained10
        nep_record.percentage10 = percentage10
        nep_record.grade10 = grade10

        nep_record.class12 = class12
        nep_record.board12 = board12
        nep_record.stream12 = stream12
        nep_record.year12 = year12
        nep_record.total_marks12 = total_marks12
        nep_record.obtained12 = obtained12
        nep_record.percentage12 = percentage12
        nep_record.grade12 = grade12

        if photo_base64:
            nep_record.photo_base64 = photo_base64
        elif not nep_record.photo_base64 and admission and admission.photo_base64:
            nep_record.photo_base64 = admission.photo_base64

        if signature_base64:
            nep_record.signature_base64 = signature_base64
        elif not nep_record.signature_base64 and admission and admission.signature_base64:
            nep_record.signature_base64 = admission.signature_base64

        nep_record.selected_courses_json = selected_courses_json

        # Payment
        nep_record.fee_amount = fee_amount
        if transaction_id:
            nep_record.transaction_id = transaction_id
            nep_record.payment_status = 'Paid'
        if payment_receipt_file:
            nep_record.payment_receipt = payment_receipt_file
        if payment_receipt_base64:
            nep_record.payment_receipt_base64 = payment_receipt_base64

        if not nep_record.application_no:
            nep_record.application_no = generate_nep_ug_application_number()

        # Handle university enrollment number: keep previous enrollment number or generate
        if not nep_record.enrollment_no:
            if previous_enrollment_no:
                nep_record.enrollment_no = previous_enrollment_no
            elif first_sem_enrollment and first_sem_enrollment.enrollment_no:
                nep_record.enrollment_no = first_sem_enrollment.enrollment_no
            elif action == 'submit':
                nep_record.enrollment_no = generate_enrollment_number()

        if action == 'submit':
            if not nep_record.transaction_id:
                messages.error(request, 'कृपया ₹500 शुल्क भुगतान पूर्ण करें एवं अपना ट्रांजेक्शन ID / UTR नंबर दर्ज करें। (Please enter your Transaction / UTR ID before submitting).')
                return redirect('nep_ug_enrollment_form')

            nep_record.status = 'Submitted'
            nep_record.is_submitted = True
            nep_record.submitted_date = timezone.now()
            nep_record.save()
            messages.success(
                request,
                f'NEP UG सत्र {nep_record.academic_session} (सेमेस्टर {nep_record.semester}) हेतु प्रवेश एवं नामांकन आवेदन सफलतापूर्वक सबमिट कर दिया गया है! आवेदन क्रमांक: {nep_record.application_no}'
            )
            return redirect('nep_ug_print', enrollment_no=nep_record.enrollment_no or nep_record.application_no)
        else:
            nep_record.status = 'Draft'
            nep_record.save()
            messages.info(request, 'NEP UG प्रवेश एवं नामांकन ड्राफ्ट सफलतापूर्वक सुरक्षित कर लिया गया है।')
            return redirect('nep_ug_enrollment_form')

    # GET Request: Pre-populate
    initial_data = {}
    if existing_nep:
        for f in [
            'application_no', 'enrollment_no', 'program_type', 'program_code', 'semester', 'academic_session',
            'previous_roll_no', 'previous_enrollment_no', 'previous_semester_result', 'previous_semester_marks',
            'full_name', 'father_name', 'mother_name', 'gender', 'dob', 'category', 'nationality',
            'religion', 'marital_status', 'blood_group', 'mobile', 'email', 'aadhaar', 'apaar_id',
            'medium', 'has_disability', 'disability_details', 'disability_percentage', 'disability_type',
            'is_minority', 'perm_state', 'perm_district', 'perm_city', 'perm_village', 'perm_pin_code',
            'corr_state', 'corr_district', 'corr_city', 'corr_village', 'corr_pin_code', 'class10',
            'board10', 'year10', 'total_marks10', 'obtained10', 'percentage10', 'grade10', 'class12',
            'board12', 'year12', 'total_marks12', 'obtained12', 'percentage12', 'grade12', 'stream12',
            'photo_base64', 'signature_base64', 'selected_courses_json',
            'fee_amount', 'payment_status', 'transaction_id', 'payment_receipt_base64'
        ]:
            val = getattr(existing_nep, f, None)
            initial_data[f] = val.isoformat() if hasattr(val, 'isoformat') else val
        if existing_nep.payment_receipt:
            try:
                initial_data['payment_receipt_url'] = existing_nep.payment_receipt.url
            except Exception:
                pass
    else:
        # Fallback to 1st sem enrollment / admission / student profile
        source = first_sem_enrollment or admission
        if source:
            for f in [
                'full_name', 'father_name', 'mother_name', 'gender', 'dob', 'category', 'nationality',
                'religion', 'marital_status', 'blood_group', 'mobile', 'email', 'aadhaar', 'apaar_id',
                'medium', 'has_disability', 'disability_details', 'disability_percentage', 'disability_type',
                'is_minority', 'perm_state', 'perm_district', 'perm_city', 'perm_village', 'perm_pin_code',
                'corr_state', 'corr_district', 'corr_city', 'corr_village', 'corr_pin_code', 'class10',
                'board10', 'year10', 'total_marks10', 'obtained10', 'percentage10', 'grade10', 'class12',
                'board12', 'year12', 'total_marks12', 'obtained12', 'percentage12', 'grade12', 'stream12',
                'photo_base64', 'signature_base64',
            ]:
                val = getattr(source, f, None)
                initial_data[f] = val.isoformat() if hasattr(val, 'isoformat') else val
        else:
            initial_data = {
                'full_name': student.full_name,
                'mobile': student.mobile,
                'email': student.email,
                'aadhaar': student.aadhaar,
            }

        # Program & semester defaults
        base_prog = _clean_ug_program_name(
            (first_sem_enrollment.program_type if first_sem_enrollment else None)
            or (admission.program_type if admission else None)
            or student.program_type
        )
        initial_data['program_type'] = base_prog
        initial_data['semester'] = 'II'
        initial_data['academic_session'] = '2026-27'
        initial_data['fee_amount'] = '500'
        initial_data['payment_status'] = 'Pending'
        initial_data['transaction_id'] = ''
        initial_data['previous_enrollment_no'] = (first_sem_enrollment.enrollment_no if first_sem_enrollment else '') or ''
        initial_data['previous_semester_result'] = 'Pass'

    # Ensure 10th details are filled if available
    if admission and not initial_data.get('board10'):
        for edu in build_education_list(admission):
            if edu.get('RowKey') == '10':
                initial_data['board10'] = edu.get('Board') or ''
                initial_data['year10'] = edu.get('Year') or ''
                initial_data['total_marks10'] = edu.get('TotalMarks') or ''
                initial_data['obtained10'] = edu.get('Obtained') or ''
                initial_data['percentage10'] = edu.get('Percentage') or ''
                initial_data['grade10'] = edu.get('Grade') or ''

    # Ensure all form fields exist in initial_data to prevent template lookup errors
    for fld in [
        'application_no', 'enrollment_no', 'previous_enrollment_no', 'previous_roll_no',
        'previous_semester_result', 'previous_semester_marks', 'full_name', 'father_name',
        'mother_name', 'gender', 'dob', 'category', 'nationality', 'religion',
        'marital_status', 'blood_group', 'mobile', 'email', 'aadhaar', 'apaar_id',
        'medium', 'has_disability', 'disability_details', 'disability_percentage',
        'disability_type', 'is_minority', 'perm_state', 'perm_district', 'perm_city',
        'perm_village', 'perm_pin_code', 'corr_state', 'corr_district', 'corr_city',
        'corr_village', 'corr_pin_code', 'class10', 'board10', 'year10', 'total_marks10',
        'obtained10', 'percentage10', 'grade10', 'class12', 'board12', 'year12',
        'total_marks12', 'obtained12', 'percentage12', 'grade12', 'stream12',
        'photo_base64', 'signature_base64', 'selected_courses_json',
        'fee_amount', 'payment_status', 'transaction_id', 'payment_receipt_url',
        'payment_receipt_base64',
    ]:
        initial_data.setdefault(fld, '')

    is_payment_done = bool(existing_nep and existing_nep.transaction_id)

    ctx = {
        'student': student,
        'admission': admission,
        'first_sem_enrollment': first_sem_enrollment,
        'existing_nep': existing_nep,
        'initial_data': initial_data,
        'is_payment_done': is_payment_done,
        'nep_program_choices': NEP_UG_PROGRAM_CHOICES,
        'semester_choices': NepUgAdmissionEnrollment.SEMESTER_CHOICES,
        'religion_choices': RELIGION_CHOICES,
        'medium_choices': MEDIUM_CHOICES,
    }
    ctx.update(get_student_sidebar_context(reg_no, active='nep_ug'))
    return render(request, 'admissions/nep_ug_form.html', ctx)


def nep_ug_print(request, enrollment_no=None):
    admin_user = request.session.get('admin_user')
    reg_no = request.session.get('reg_no')
    if not reg_no and not admin_user:
        return redirect('login')

    nep_record = None
    if enrollment_no:
        nep_record = NepUgAdmissionEnrollment.objects.filter(
            models.Q(enrollment_no=enrollment_no)
            | models.Q(application_no=enrollment_no)
            | models.Q(pk=int(enrollment_no) if str(enrollment_no).isdigit() else -1)
        ).first()

    if admin_user:
        if not nep_record:
            if enrollment_no:
                nep_record = get_object_or_404(NepUgAdmissionEnrollment, enrollment_no=enrollment_no)
            elif reg_no:
                nep_record = NepUgAdmissionEnrollment.objects.filter(reg_no=reg_no, is_submitted=True).order_by('-submitted_date').first()
                if not nep_record:
                    nep_record = get_object_or_404(NepUgAdmissionEnrollment, reg_no=reg_no)
            else:
                messages.error(request, 'NEP UG Admission cum Enrollment record not found.')
                return redirect('manage_nepug_enrollments')
        student = nep_record.student
    else:
        student = get_object_or_404(Student, registration_no=reg_no)
        if not nep_record:
            if enrollment_no:
                nep_record = get_object_or_404(NepUgAdmissionEnrollment, reg_no=reg_no)
            else:
                nep_record = NepUgAdmissionEnrollment.objects.filter(reg_no=reg_no, is_submitted=True).order_by('-submitted_date').first()
                if not nep_record:
                    messages.warning(request, 'No submitted NEP UG application found. Please complete the form first.')
                    return redirect('nep_ug_enrollment_form')
        elif nep_record.reg_no != reg_no:
            raise Http404("No NEP UG Record matches the given query.")

    ctx = {
        'student': student,
        'nep': nep_record,
    }
    if reg_no and not admin_user:
        ctx.update(get_student_sidebar_context(reg_no, active='nep_ug'))
    return render(request, 'admissions/nep_ug_print.html', ctx)


def nep_ug_fee_receipt(request, enrollment_no=None):
    admin_user = request.session.get('admin_user')
    reg_no = request.session.get('reg_no')
    if not reg_no and not admin_user:
        return redirect('login')

    nep_record = None
    if enrollment_no:
        nep_record = NepUgAdmissionEnrollment.objects.filter(
            models.Q(enrollment_no=enrollment_no)
            | models.Q(application_no=enrollment_no)
            | models.Q(pk=int(enrollment_no) if str(enrollment_no).isdigit() else -1)
        ).first()

    if admin_user:
        if not nep_record:
            if enrollment_no:
                nep_record = get_object_or_404(NepUgAdmissionEnrollment, enrollment_no=enrollment_no)
            elif reg_no:
                nep_record = NepUgAdmissionEnrollment.objects.filter(reg_no=reg_no, is_submitted=True).order_by('-submitted_date').first()
                if not nep_record:
                    nep_record = get_object_or_404(NepUgAdmissionEnrollment, reg_no=reg_no)
            else:
                messages.error(request, 'NEP UG Record not found.')
                return redirect('manage_nepug_enrollments')
        student = nep_record.student
    else:
        student = get_object_or_404(Student, registration_no=reg_no)
        if not nep_record:
            if enrollment_no:
                nep_record = get_object_or_404(NepUgAdmissionEnrollment, reg_no=reg_no)
            else:
                nep_record = NepUgAdmissionEnrollment.objects.filter(reg_no=reg_no, is_submitted=True).order_by('-submitted_date').first()
                if not nep_record:
                    messages.warning(request, 'No submitted NEP UG application found.')
                    return redirect('nep_ug_enrollment_form')
        elif nep_record.reg_no != reg_no:
            raise Http404("No NEP UG Record matches the given query.")

    sub_date = nep_record.submitted_date or timezone.now()
    deposit_date = sub_date.strftime('%d/%m/%Y at %I:%M %p')
    month_year = sub_date.strftime('%b. / %Y').upper()

    program_display = f"{nep_record.program_type} ({nep_record.semester_display})"

    ctx = {
        'student': student,
        'nep': nep_record,
        'program_display': program_display,
        'deposit_date': deposit_date,
        'month_year': month_year,
        'fee_amount': nep_record.fee_amount or '500',
        'transaction_id': nep_record.transaction_id or '',
        'payment_status': nep_record.payment_status or ('Paid' if nep_record.transaction_id else 'Pending'),
    }
    return render(request, 'admissions/nep_ug_receipt.html', ctx)


@student_login_required
@require_http_methods(['POST'])
def cancel_nep_ug_enrollment(request):
    reg_no = request.session.get('reg_no')
    nep_record = NepUgAdmissionEnrollment.objects.filter(reg_no=reg_no).order_by('-submitted_date', '-created_at').first()
    if not nep_record:
        messages.error(request, 'No NEP UG application found to cancel.')
        return redirect('student_dashboard')

    if nep_record.status == 'Approved':
        messages.error(
            request,
            'Cannot cancel application. Your NEP UG application has already been accepted/approved by the college administration.'
        )
        return redirect('student_dashboard')

    nep_record.status = 'Draft'
    nep_record.is_submitted = False
    nep_record.save(update_fields=['status', 'is_submitted', 'updated_at'])

    messages.success(
        request,
        'NEP UG admission application reset to Draft successfully. You can now edit any details and re-submit your form.'
    )
    return redirect('nep_ug_enrollment_form')
