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







