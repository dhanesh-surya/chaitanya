from django.test import TestCase
from django.urls import reverse
from accounts.models import Student
from admissions.models import StudentAdmission, StudentEnrollment
from admissions.utils import generate_enrollment_number


class StudentEnrollmentModelTestCase(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            registration_no='REG1001',
            full_name='Test Student',
            email='teststudent@example.com',
            password='password123',
        )

    def test_generate_enrollment_number(self):
        num1 = generate_enrollment_number()
        self.assertEqual(num1, 'CCP26050001')

        enrollment = StudentEnrollment.objects.create(
            enrollment_no=num1,
            reg_no=self.student.registration_no,
            student=self.student,
            full_name='Test Student',
            status='Submitted',
            is_submitted=True,
        )
        num2 = generate_enrollment_number()
        self.assertEqual(num2, 'CCP26050002')


class EnrollmentViewsTestCase(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            registration_no='AS26090001',
            full_name='Pooja Soni',
            email='poojasoni@example.com',
            mobile='9876543210',
            password='password123',
        )
        self.admission = StudentAdmission.objects.create(
            reg_no='AS26090001',
            application_no='CCP2609260001',
            full_name='Pooja Soni',
            father_name='Ramesh Soni',
            mother_name='Sita Soni',
            gender='Female',
            category='OBC',
            dob='2003-12-19',
            mobile='9876543210',
            email='poojasoni@example.com',
            aadhaar='123456789012',
            perm_state='Chhattisgarh',
            perm_district='Janjgir-Champa',
            perm_city='Pamgarh',
            perm_pin_code='495554',
            class10='10th',
            board10='CGBSE',
            year10=2019,
            total_marks10='600',
            obtained10='480',
            percentage10='80',
            photo_base64='data:image/jpeg;base64,/9j/fakephoto',
            signature_base64='data:image/jpeg;base64,/9j/fakesig',
            program_type='B.A. First Semester',
            status='Submitted',
            is_submitted=True,
        )

    def test_enrollment_form_get_prepopulation(self):
        session = self.client.session
        session['is_logged_in'] = True
        session['reg_no'] = self.student.registration_no
        session.save()

        response = self.client.get(reverse('enrollment_form'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['initial_data']['full_name'], 'Pooja Soni')
        self.assertEqual(response.context['initial_data']['father_name'], 'Ramesh Soni')
        self.assertEqual(response.context['initial_data']['photo_base64'], 'data:image/jpeg;base64,/9j/fakephoto')

    def test_enrollment_form_post_submit(self):
        session = self.client.session
        session['is_logged_in'] = True
        session['reg_no'] = self.student.registration_no
        session.save()

        courses_json = '[{"code": "HNSC-01", "name": "Hindi Sahitya Ka Itihas", "paper": "I", "type_1": "Theory", "type_2": "DSC", "dept": "Hindi"}]'
        payload = {
            'action': 'submit',
            'full_name': 'Pooja Soni Updated',
            'father_name': 'Ramesh Soni',
            'mother_name': 'Sita Soni',
            'gender': 'Female',
            'dob': '2003-12-19',
            'category': 'OBC',
            'mobile': '9876543210',
            'email': 'poojasoni@example.com',
            'aadhaar': '123456789012',
            'perm_state': 'Chhattisgarh',
            'perm_district': 'Janjgir-Champa',
            'perm_city': 'Pamgarh',
            'perm_pin_code': '495554',
            'class10': '10th',
            'board10': 'CGBSE',
            'year10': '2019',
            'total_marks10': '600',
            'obtained10': '480',
            'percentage10': '80',
            'photo_base64': 'data:image/jpeg;base64,/9j/fakephoto',
            'signature_base64': 'data:image/jpeg;base64,/9j/fakesig',
            'program_type': 'B.A. First Semester',
            'program_code': 'CCBA01',
            'selected_courses_json': courses_json,
            'fee_amount': '500',
            'transaction_id': 'TXN1234567890',
        }
        response = self.client.post(reverse('enrollment_form'), payload)
        self.assertEqual(response.status_code, 302)

        enrollment = StudentEnrollment.objects.filter(reg_no=self.student.registration_no).first()
        self.assertIsNotNone(enrollment)
        self.assertTrue(enrollment.is_submitted)
        self.assertTrue(enrollment.enrollment_no.startswith('CCP2605'))
        self.assertEqual(enrollment.full_name, 'Pooja Soni Updated')

    def test_enrollment_print_view(self):
        enrollment = StudentEnrollment.objects.create(
            enrollment_no='CCP26050001',
            reg_no=self.student.registration_no,
            student=self.student,
            full_name='Pooja Soni',
            status='Submitted',
            is_submitted=True,
            selected_courses_json='[{"code": "HNSC-01", "name": "Hindi Sahitya Ka Itihas", "paper": "I", "type_1": "Theory", "type_2": "DSC"}]',
        )
        session = self.client.session
        session['is_logged_in'] = True
        session['reg_no'] = self.student.registration_no
        session.save()

        response = self.client.get(reverse('enrollment_print', kwargs={'enrollment_no': 'CCP26050001'}))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('Chaitanya Science &amp; Arts College, Pamgarh', content)
        self.assertIn('(An Autonomous Institution Approved by UGC)', content)
        self.assertIn('STUDENT ENROLLMENT APPLICATION (SESSION 2026-27)', content)
        self.assertIn('CCP26050001', content)
        self.assertIn('HNSC-01', content)

    def test_ug_student_does_not_show_ug_qualification(self):
        session = self.client.session
        session['is_logged_in'] = True
        session['reg_no'] = self.student.registration_no
        session.save()

        # Before payment, section 3 & course selection are locked
        response_before = self.client.get(reverse('enrollment_form'))
        self.assertEqual(response_before.status_code, 200)
        self.assertFalse(response_before.context['is_payment_done'])
        content_before = response_before.content.decode('utf-8')
        self.assertIn('अभी लॉक हैं', content_before)

        # After payment, section 3 & course selection are unlocked
        StudentEnrollment.objects.create(
            reg_no=self.student.registration_no,
            student=self.student,
            transaction_id='TXN_PAID_123',
            fee_amount='500',
            status='Draft',
        )
        response_after = self.client.get(reverse('enrollment_form'))
        self.assertEqual(response_after.status_code, 200)
        self.assertTrue(response_after.context['is_payment_done'])
        self.assertFalse(response_after.context['show_ug_qualification'])
        content_after = response_after.content.decode('utf-8')
        self.assertNotIn('Undergraduate / Graduation Qualification', content_after)
        self.assertIn('Fixed as applied in Admission', content_after)
        self.assertIn('id="ddlProgramLevel" class="modern-select" disabled', content_after)
        self.assertIn('id="ddlProgramType" class="modern-select" disabled', content_after)

    def test_pg_student_shows_ug_qualification_and_saves_it(self):
        pg_student = Student.objects.create(
            registration_no='PG26090002',
            full_name='Amar Kumar',
            email='amar@example.com',
            mobile='9876543211',
            password='password123',
        )
        StudentAdmission.objects.create(
            reg_no='PG26090002',
            application_no='CCP2609260002',
            full_name='Amar Kumar',
            mobile='9876543211',
            email='amar@example.com',
            program_type='M.Sc. Computer Science - First Semester',
            status='Submitted',
            is_submitted=True,
            education_json='[{"RowKey": "10", "ClassName": "10th", "Board": "CGBSE", "Year": "2019", "Percentage": "82"}, {"RowKey": "12", "ClassName": "12th", "Board": "CGBSE", "Stream": "Science", "Year": "2021", "Percentage": "78"}, {"RowKey": "grad", "ClassName": "B.Sc. CS", "Board": "ABVV", "Stream": "Computer Science", "Year": "2024", "TotalMarks": "1800", "Obtained": "1440", "Percentage": "80", "Grade": "First"}]',
            selected_subjects_json='[{"name": "Advanced Computer Networking", "type1": "Theory", "type2": "Theory"}]',
        )

        session = self.client.session
        session['is_logged_in'] = True
        session['reg_no'] = pg_student.registration_no
        session.save()

        # GET request
        response = self.client.get(reverse('enrollment_form'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['show_ug_qualification'])
        content = response.content.decode('utf-8')
        self.assertIn('name="class_grad"', content)
        self.assertEqual(response.context['initial_data']['class_grad'], 'B.Sc. CS')
        self.assertEqual(response.context['initial_data']['board_grad'], 'ABVV')
        self.assertEqual(response.context['initial_data']['stream_grad'], 'Computer Science')

        # POST submission saves graduation details and retains admission courses
        post_payload = {
            'action': 'submit',
            'full_name': 'Amar Kumar',
            'father_name': 'Ram Kumar',
            'mother_name': 'Maya Devi',
            'dob': '2001-05-15',
            'gender': 'Male',
            'category': 'General',
            'mobile': '9876543211',
            'email': 'amar@example.com',
            'aadhaar': '987654321098',
            'class10': '10th',
            'board10': 'CGBSE',
            'year10': '2019',
            'class12': '12th',
            'board12': 'CGBSE',
            'stream12': 'Science',
            'year12': '2021',
            'class_grad': 'B.Sc. Computer Science',
            'board_grad': 'ABVV Bilaspur',
            'stream_grad': 'Computer Science',
            'year_grad': '2024',
            'total_marks_grad': '1800',
            'obtained_grad': '1440',
            'percentage_grad': '80',
            'grade_grad': 'First',
            'fee_amount': '500',
            'transaction_id': 'TXN9988776655',
            # Even if program_type/selected_courses_json omitted because selects/inputs were disabled:
        }
        res_post = self.client.post(reverse('enrollment_form'), post_payload)
        self.assertEqual(res_post.status_code, 302)

        enrollment = StudentEnrollment.objects.filter(reg_no='PG26090002').first()
        self.assertIsNotNone(enrollment)
        self.assertEqual(enrollment.class_grad, 'B.Sc. Computer Science')
        self.assertEqual(enrollment.board_grad, 'ABVV Bilaspur')
        self.assertEqual(enrollment.stream_grad, 'Computer Science')
        self.assertEqual(enrollment.percentage_grad, '80')
        # Section E fallback preserved from admission
        self.assertEqual(enrollment.program_type, 'M.Sc. Computer Science - First Semester')
        self.assertIn('Advanced Computer Networking', enrollment.selected_courses_json)

        # Print slip shows graduation row
        res_print = self.client.get(reverse('enrollment_print', kwargs={'enrollment_no': enrollment.enrollment_no}))
        self.assertEqual(res_print.status_code, 200)
        print_content = res_print.content.decode('utf-8')
        self.assertIn('B.Sc. Computer Science', print_content)
        self.assertIn('ABVV Bilaspur', print_content)
        self.assertIn('80%', print_content)


class CancelEnrollmentTestCase(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            registration_no='REG2001',
            full_name='Rahul Sharma',
            email='rahul@example.com',
            mobile='9876543210',
            password='password123',
        )
        self.admission = StudentAdmission.objects.create(
            reg_no=self.student.registration_no,
            application_no='APP2001',
            full_name='Rahul Sharma',
            status='Approved',
            is_submitted=True,
        )
        self.enrollment = StudentEnrollment.objects.create(
            enrollment_no='ENR2001',
            reg_no=self.student.registration_no,
            student=self.student,
            admission=self.admission,
            full_name='Rahul Sharma',
            program_type='B.Sc. First Semester',
            status='Submitted',
            is_submitted=True,
        )

    def _login_student(self):
        session = self.client.session
        session['is_logged_in'] = True
        session['reg_no'] = self.student.registration_no
        session.save()

    def test_dashboard_shows_cancel_enrollment_before_admin_accepts(self):
        self._login_student()

        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('Cancel Enrollment', content)
        self.assertTrue(response.context['can_cancel_enrollment'])

    def test_student_can_cancel_enrollment_before_admin_accepts(self):
        session = self.client.session
        session['is_logged_in'] = True
        session['reg_no'] = self.student.registration_no
        session.save()

        # POST to cancel enrollment
        response = self.client.post(reverse('cancel_enrollment'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('enrollment_form'))

        # Check DB status reverted to Draft and is_submitted=False
        self.enrollment.refresh_from_db()
        self.assertEqual(self.enrollment.status, 'Draft')
        self.assertFalse(self.enrollment.is_submitted)

        # GET enrollment_form is now editable (not redirected to print)
        get_form = self.client.get(reverse('enrollment_form'))
        self.assertEqual(get_form.status_code, 200)

        # Dashboard now shows "Edit / Complete Enrollment" instead of "Cancel Enrollment"
        res_dash = self.client.get(reverse('student_dashboard'))
        self.assertEqual(res_dash.status_code, 200)
        self.assertFalse(res_dash.context['can_cancel_enrollment'])
        dash_content = res_dash.content.decode('utf-8')
        self.assertNotIn('Cancel Enrollment', dash_content)
        self.assertIn('Edit / Complete Enrollment', dash_content)

    def test_student_cannot_cancel_enrollment_after_admin_accepts(self):
        # Admin accepts enrollment
        self.enrollment.status = 'Approved'
        self.enrollment.save()

        session = self.client.session
        session['is_logged_in'] = True
        session['reg_no'] = self.student.registration_no
        session.save()

        # Dashboard shows locked status, NO cancel button
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['can_cancel_enrollment'])
        content = response.content.decode('utf-8')
        self.assertNotIn('Cancel Enrollment', content)
        self.assertIn('Enrollment Accepted (Locked)', content)

        # Attempt to cancel via POST should be rejected
        post_response = self.client.post(reverse('cancel_enrollment'))
        self.assertEqual(post_response.status_code, 302)
        self.assertRedirects(post_response, reverse('student_dashboard'))

        # DB status remains Approved and is_submitted remains True
        self.enrollment.refresh_from_db()
        self.assertEqual(self.enrollment.status, 'Approved')
        self.assertTrue(self.enrollment.is_submitted)

    def test_admin_update_enrollment_status(self):
        # Login as admin
        admin_session = self.client.session
        admin_session['admin_user'] = 'admin'
        admin_session.save()

        # Admin approves enrollment
        resp_approve = self.client.post(
            reverse('update_enrollment_status', kwargs={'pk': self.enrollment.pk}),
            {'status': 'Approved'}
        )
        self.assertEqual(resp_approve.status_code, 302)
        self.enrollment.refresh_from_db()
        self.assertEqual(self.enrollment.status, 'Approved')
        self.assertTrue(self.enrollment.is_submitted)

        # Admin resets to Draft
        resp_draft = self.client.post(
            reverse('update_enrollment_status', kwargs={'pk': self.enrollment.pk}),
            {'status': 'Draft'}
        )
        self.assertEqual(resp_draft.status_code, 302)
        self.enrollment.refresh_from_db()
        self.assertEqual(self.enrollment.status, 'Draft')
        self.assertFalse(self.enrollment.is_submitted)

    def test_enrollment_print_defaults_paper_to_I_and_resolves_course_code(self):
        from courses.models import ProgramCourse
        import json

        ProgramCourse.objects.create(
            program_type='B.A. First Semester',
            department='Hindi',
            course_name='Hindi Sahitya Ka Itihas',
            course_code='HNSC-01',
            paper_no='I',
            course_type_1='Theory',
            course_type_2='DSC',
        )

        self.enrollment.program_type = 'B.A. First Semester'
        self.enrollment.selected_courses_json = json.dumps([
            {
                'name': 'Hindi — Hindi Sahitya',
                'dept': 'Hindi',
                'type_1': 'Theory',
                'type_2': 'DSC',
                'code': '',
                'paper': '',
            },
            {
                'name': 'Sociology — Introduction to Sociology',
                'dept': 'Sociology',
                'type_1': 'Theory',
                'type_2': 'DSC',
                'code': 'SOSC-01',
                'paper': 'II',
            },
            {
                'name': 'Generic Elective Course',
                'dept': 'Forestry',
                'type_1': 'Theory',
                'type_2': 'GE',
                'code': '',
                'paper': '',
            }
        ])
        self.enrollment.save()

        self._login_student()
        response = self.client.get(reverse('enrollment_print', kwargs={'enrollment_no': self.enrollment.enrollment_no}))
        self.assertEqual(response.status_code, 200)

        courses = response.context['enrolled_courses']
        # Hindi should resolve code to HNSC-01 and paper to I
        self.assertEqual(courses[0]['code'], 'HNSC-01')
        self.assertEqual(courses[0]['paper'], 'I')

        # Sociology preserves paper II
        self.assertEqual(courses[1]['paper'], 'II')

        # Generic Elective with blank paper defaults to I
        self.assertEqual(courses[2]['paper'], 'I')

    def test_enrollment_form_renders_course_code_column(self):
        self.enrollment.is_submitted = False
        self.enrollment.status = 'Draft'
        self.enrollment.transaction_id = 'TXN_COURSE_CODE_123'
        self.enrollment.save()

        self._login_student()
        response = self.client.get(reverse('enrollment_form'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('Course Code', content)

    def test_progressive_payment_unlocks_section3_and_courses(self):
        """Verifies section 3 and further sections are locked until payment is submitted."""
        self.enrollment.delete()  # Start with no enrollment
        self._login_student()

        # Step 1: GET enrollment_form before payment
        res1 = self.client.get(reverse('enrollment_form'))
        self.assertEqual(res1.status_code, 200)
        self.assertFalse(res1.context['is_payment_done'])
        self.assertIn('अभी लॉक हैं', res1.content.decode('utf-8'))
        self.assertNotIn('id="section3Card"', res1.content.decode('utf-8'))

        # Step 2: POST save_payment with UTR and checkbox
        res2 = self.client.post(reverse('enrollment_form'), {
            'action': 'save_payment',
            'transaction_id': 'UTR998877665544',
            'fee_amount': '500',
            'info_correctness': 'on',
        })
        self.assertEqual(res2.status_code, 302)
        self.assertIn('step=section3', res2.url)

        # Step 3: GET enrollment_form after payment
        res3 = self.client.get(reverse('enrollment_form'))
        self.assertEqual(res3.status_code, 200)
        self.assertTrue(res3.context['is_payment_done'])
        content3 = res3.content.decode('utf-8')
        self.assertIn('id="section3Card"', content3)
        self.assertIn('Section E: Enrolled Program', content3)
        self.assertIn('UTR: <strong style="font-family: monospace; color: #082B49;">UTR998877665544</strong>', content3)


    def test_enrollment_form_header_visibility_and_instructions_modal(self):
        from admissions.models import EnrollmentInstruction
        instr = EnrollmentInstruction.objects.filter(is_active=True).first()
        if not instr:
            instr = EnrollmentInstruction.objects.create(
                title="छात्र नामांकन प्रक्रिया",
                college_title="चैतन्य कॉलेज",
                content_html="<p>चरण 1: निर्देश</p>",
                is_active=True,
            )
        self.enrollment.is_submitted = False
        self.enrollment.save()

        session = self.client.session
        session['is_logged_in'] = True
        session['reg_no'] = self.student.registration_no
        session.save()

        response = self.client.get(reverse('enrollment_form'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('enrollment-header-card', content)
        self.assertIn('Student Enrollment Form (छात्र नामांकन फॉर्म)', content)
        self.assertNotIn('Student_Enrollment_User_Guide.pdf', content)
        self.assertNotIn('Enrollment Guide (PDF)', content)
        self.assertIn('नामांकन निर्देश (Instructions)', content)
        self.assertIn('id="enrollmentGuideModal"', content)
        self.assertIn('चरण 1', content)


class NepUgAdmissionEnrollmentTestCase(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            registration_no='NEP26001',
            full_name='Vikash Sharma',
            email='vikash@example.com',
            mobile='9826100001',
            password='password123',
            program_type='B.Sc. First Semester',
        )
        self.admission = StudentAdmission.objects.create(
            reg_no='NEP26001',
            application_no='CCP26090001',
            full_name='Vikash Sharma',
            father_name='Sunil Sharma',
            mother_name='Geeta Sharma',
            gender='Male',
            category='General',
            dob='2004-05-15',
            mobile='9826100001',
            email='vikash@example.com',
            program_type='B.Sc. First Semester',
            status='Approved',
            is_submitted=True,
        )
        self.first_sem_enrollment = StudentEnrollment.objects.create(
            reg_no='NEP26001',
            enrollment_no='CCP26059999',
            student=self.student,
            admission=self.admission,
            full_name='Vikash Sharma',
            father_name='Sunil Sharma',
            mother_name='Geeta Sharma',
            gender='Male',
            status='Approved',
            is_submitted=True,
        )

    def test_nep_ug_student_access_and_render(self):
        # Student visiting /admission/nep-ug/ renders form with left sidebar & right form
        session = self.client.session
        session['is_logged_in'] = True
        session['reg_no'] = self.student.registration_no
        session.save()

        response = self.client.get(reverse('nep_ug_enrollment_form'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('portal-layout', response.content.decode('utf-8'))
        self.assertIn('portal-sidebar', response.content.decode('utf-8'))
        self.assertIn('/admin/nep-ug/', response.content.decode('utf-8'))
        self.assertEqual(response.context['initial_data']['full_name'], 'Vikash Sharma')

    def test_nep_ug_admin_create_and_print(self):
        from accounts.models import AdminUser
        from admissions.models import NepUgAdmissionEnrollment

        AdminUser.objects.create(username='admin', password='password123')
        session = self.client.session
        session['admin_user'] = 'admin'
        session.save()

        # 1. Test GET with lookup
        lookup_res = self.client.get(reverse('admin_create_nepug') + f'?reg_no={self.student.registration_no}')
        self.assertEqual(lookup_res.status_code, 200)
        self.assertEqual(lookup_res.context['initial_data']['full_name'], 'Vikash Sharma')
        self.assertEqual(lookup_res.context['initial_data']['previous_enrollment_no'], 'CCP26059999')

        # 2. Test POST create
        payload = {
            'reg_no': self.student.registration_no,
            'full_name': 'Vikash Sharma',
            'father_name': 'Sunil Sharma',
            'mother_name': 'Geeta Sharma',
            'gender': 'Male',
            'dob': '2004-05-15',
            'category': 'General',
            'medium': 'Hindi',
            'mobile': '9826100001',
            'email': 'vikash@example.com',
            'semester': 'II',
            'program_type': 'B.Sc. Bio Group',
            'academic_session': '2026-27',
            'previous_roll_no': '26001234',
            'previous_enrollment_no': 'CCP26059999',
            'previous_semester_result': 'Pass',
            'previous_semester_marks': '450/600',
            'corr_village': 'Pamgarh Main Road',
            'corr_district': 'Janjgir-Champa',
            'corr_state': 'Chhattisgarh',
            'corr_pin_code': '495554',
            'fee_amount': '500',
            'transaction_id': 'UTR123456789012',
            'payment_status': 'Paid',
            'status': 'Approved',
        }
        res = self.client.post(reverse('admin_create_nepug'), payload)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('manage_nepug_enrollments'))

        record = NepUgAdmissionEnrollment.objects.filter(reg_no='NEP26001').first()
        self.assertIsNotNone(record)
        self.assertEqual(record.status, 'Approved')
        self.assertTrue(record.is_submitted)
        self.assertEqual(record.transaction_id, 'UTR123456789012')
        self.assertEqual(record.enrollment_no, 'CCP26059999')
        self.assertTrue(record.application_no.startswith('NEP'))

        # Check Admin Print Slip
        print_res = self.client.get(reverse('admin_print_nepug', kwargs={'pk': record.pk}))
        self.assertEqual(print_res.status_code, 200)
        self.assertIn('NEP UG ADMISSION CUM ENROLLMENT SLIP', print_res.content.decode('utf-8'))

        # Check Admin Receipt
        receipt_res = self.client.get(reverse('admin_receipt_nepug', kwargs={'pk': record.pk}))
        self.assertEqual(receipt_res.status_code, 200)
        self.assertIn('NEP UG FEE RECEIPT', receipt_res.content.decode('utf-8'))

    def test_nep_ug_admin_management_and_export(self):
        from accounts.models import AdminUser
        from admissions.models import NepUgAdmissionEnrollment

        AdminUser.objects.create(username='admin', password='password123')
        session = self.client.session
        session['admin_user'] = 'admin'
        session.save()

        rec = NepUgAdmissionEnrollment.objects.create(
            student=self.student,
            reg_no='NEP26001',
            application_no='NEP26090001',
            enrollment_no='CCP26059999',
            program_type='B.Sc. Bio Group',
            semester='II',
            full_name='Vikash Sharma',
            father_name='Sunil Sharma',
            gender='Male',
            status='Submitted',
            is_submitted=True,
            transaction_id='UTR123456789012',
        )

        # 1. Manage NEPUG list
        list_res = self.client.get(reverse('manage_nepug_enrollments'))
        self.assertEqual(list_res.status_code, 200)
        self.assertIn('Vikash Sharma', list_res.content.decode('utf-8'))
        self.assertIn('NEPUG', list_res.content.decode('utf-8'))

        # 2. Update status
        up_res = self.client.post(reverse('update_nepug_status', kwargs={'pk': rec.pk}), {'status': 'Approved'})
        self.assertEqual(up_res.status_code, 302)
        rec.refresh_from_db()
        self.assertEqual(rec.status, 'Approved')

        # 3. Export Excel
        export_res = self.client.get(reverse('export_nepug_excel'))
        self.assertEqual(export_res.status_code, 200)
        self.assertEqual(
            export_res['Content-Type'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    def test_nep_ug_education_qualifications_and_photo_signature(self):
        from accounts.models import AdminUser
        from admissions.models import NepUgAdmissionEnrollment
        import json

        AdminUser.objects.create(username='admin', password='password123')
        session = self.client.session
        session['admin_user'] = 'admin'
        session.save()

        # Update student admission with education details and photo
        self.admission.class10 = '10th'
        self.admission.board10 = 'CGBSE'
        self.admission.year10 = 2022
        self.admission.total_marks10 = '600'
        self.admission.obtained10 = '510'
        self.admission.percentage10 = '85'
        self.admission.class12 = '12th'
        self.admission.board12 = 'CGBSE'
        self.admission.year12 = 2024
        self.admission.total_marks12 = '500'
        self.admission.obtained12 = '420'
        self.admission.percentage12 = '84'
        self.admission.photo_base64 = 'data:image/jpeg;base64,mockphoto101'
        self.admission.signature_base64 = 'data:image/jpeg;base64,mocksign101'
        self.admission.save()

        # 1. Lookup pre-fill check
        lookup_res = self.client.get(reverse('admin_create_nepug') + f'?reg_no={self.student.registration_no}')
        self.assertEqual(lookup_res.status_code, 200)
        init_data = lookup_res.context['initial_data']
        self.assertEqual(init_data['class10'], '10th')
        self.assertEqual(init_data['board10'], 'CGBSE')
        self.assertEqual(init_data['percentage10'], '85')
        self.assertEqual(init_data['percentage12'], '84')
        self.assertEqual(init_data['photo_base64'], 'data:image/jpeg;base64,mockphoto101')

        # 2. POST create with previous UG marksheet & base64 photo/signature
        payload = {
            'reg_no': self.student.registration_no,
            'full_name': 'Vikash Sharma',
            'father_name': 'Sunil Sharma',
            'mother_name': 'Geeta Sharma',
            'gender': 'Male',
            'dob': '2004-05-15',
            'category': 'General',
            'medium': 'Hindi',
            'mobile': '9826100001',
            'email': 'vikash@example.com',
            'semester': 'II',
            'program_type': 'B.Sc. Bio Group',
            'academic_session': '2026-27',
            'previous_roll_no': '26001234',
            'previous_enrollment_no': 'CCP26059999',
            'previous_semester_result': 'Pass',
            'previous_semester_marks': '450/600',
            # 10th
            'class10': '10th',
            'board10': 'CGBSE',
            'year10': '2022',
            'total_marks10': '600',
            'obtained10': '510',
            'percentage10': '85',
            # 12th
            'class12': '12th',
            'board12': 'CGBSE',
            'stream12': 'Science Bio',
            'year12': '2024',
            'total_marks12': '500',
            'obtained12': '420',
            'percentage12': '84',
            # Previous UG Marksheet
            'previous_exam_name': 'B.Sc. First Semester',
            'previous_board': 'Autonomous Exam Cell, CSAC Pamgarh',
            'previous_year': '2025',
            'previous_total_marks': '600',
            'previous_obtained_marks': '480',
            'previous_percentage': '80.00',
            # Photos
            'photo_base64': 'data:image/jpeg;base64,mockphoto101',
            'signature_base64': 'data:image/jpeg;base64,mocksign101',
            'fee_amount': '500',
            'transaction_id': 'UTR5544332211',
            'payment_status': 'Paid',
            'status': 'Approved',
        }
        res = self.client.post(reverse('admin_create_nepug'), payload)
        self.assertEqual(res.status_code, 302)

        record = NepUgAdmissionEnrollment.objects.filter(reg_no='NEP26001').first()
        self.assertIsNotNone(record)
        self.assertEqual(record.previous_exam_name, 'B.Sc. First Semester')
        self.assertEqual(record.previous_board, 'Autonomous Exam Cell, CSAC Pamgarh')
        self.assertEqual(record.previous_percentage, '80.00')
        self.assertEqual(record.photo_base64, 'data:image/jpeg;base64,mockphoto101')
        self.assertEqual(record.signature_base64, 'data:image/jpeg;base64,mocksign101')

        # Check education_json structured data
        edu_list = json.loads(record.education_json)
        self.assertEqual(len(edu_list), 3)
        self.assertEqual(edu_list[0]['className'], '10th')
        self.assertEqual(edu_list[1]['className'], '12th')
        self.assertEqual(edu_list[2]['className'], 'B.Sc. First Semester')

        # 3. Verify student at /admission/enrollment/ sees NEP UG card without breaking Sem I
        student_session = self.client.session
        student_session['is_logged_in'] = True
        student_session['reg_no'] = self.student.registration_no
        student_session.save()

        portal_res = self.client.get(reverse('enrollment_form'), follow=True)
        self.assertEqual(portal_res.status_code, 200)
        portal_content = portal_res.content.decode('utf-8')
        self.assertIn('NEP UG Semester II', portal_content)
        self.assertIn(record.application_no, portal_content)

        # 4. Verify admin students list displays NEP UG badge and print slip link
        admin_session = self.client.session
        admin_session['admin_user'] = 'admin'
        admin_session.save()

        students_res = self.client.get(reverse('manage_students') + f'?search={self.student.registration_no}')
        self.assertEqual(students_res.status_code, 200)
        students_content = students_res.content.decode('utf-8')
        self.assertIn('NEP Sem II: Approved', students_content)
        self.assertIn(f'/admin/nep-ug/print/{record.pk}/', students_content)


