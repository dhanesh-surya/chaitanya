from django.test import TestCase
from django.urls import reverse

from accounts.models import AdminUser, Student


class ManageStudentsProgramFilterTestCase(TestCase):
    def setUp(self):
        self.admin = AdminUser.objects.create(
            username='admin',
            password='adminpassword',
        )
        self.student_bsc = Student.objects.create(
            registration_no='BSC001',
            full_name='Amit Verma',
            email='amit@example.com',
            program_type='B.Sc. First Semester',
            course_name='B.Sc.',
        )
        self.student_ba = Student.objects.create(
            registration_no='BA001',
            full_name='Priya Singh',
            email='priya@example.com',
            program_type='B.A. First Semester',
            course_name='B.A.',
        )

    def _login_admin(self):
        session = self.client.session
        session['admin_user'] = 'admin'
        session.save()

    def test_default_students_page_is_blank_and_prompts_to_select_program(self):
        self._login_admin()
        response = self.client.get(reverse('manage_students'))
        self.assertEqual(response.status_code, 200)

        # By default, no students are loaded
        self.assertEqual(len(response.context['students']), 0)
        self.assertEqual(response.context['total_count'], 0)
        self.assertEqual(response.context['program_filter'], '')

        content = response.content.decode('utf-8')
        # "All Programs" must be removed
        self.assertNotIn('All Programs', content)
        # "-- Select Program --" option should be present
        self.assertIn('-- Select Program --', content)
        # Empty state message indicating no program selected
        self.assertIn('No Program Selected', content)
        self.assertIn('Please select a program from the dropdown above to see details.', content)

    def test_students_details_load_when_program_selected(self):
        self._login_admin()
        response = self.client.get(reverse('manage_students') + '?program=B.Sc.+First+Semester')
        self.assertEqual(response.status_code, 200)

        # Only B.Sc. students loaded
        self.assertEqual(len(response.context['students']), 1)
        self.assertEqual(response.context['students'][0].registration_no, 'BSC001')
        self.assertEqual(response.context['total_count'], 1)

        content = response.content.decode('utf-8')
        self.assertIn('Amit Verma', content)
        self.assertNotIn('Priya Singh', content)

    def test_export_csv_without_program_warns_and_redirects(self):
        self._login_admin()
        response = self.client.get(reverse('export_students_csv'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('manage_students'))

    def test_export_csv_with_program(self):
        self._login_admin()
        response = self.client.get(reverse('export_students_csv') + '?program=B.Sc.+First+Semester')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        content = response.content.decode('utf-8')
        self.assertIn('BSC001', content)
        self.assertIn('Amit Verma', content)
        self.assertNotIn('BA001', content)

    def test_admin_can_print_slip_for_any_student_enrollment(self):
        from admissions.models import StudentEnrollment

        enrollment = StudentEnrollment.objects.create(
            enrollment_no='CCP990001',
            reg_no='BSC001',
            student=self.student_bsc,
            full_name='Amit Verma',
            program_type='B.Sc. First Semester',
            is_submitted=True,
            status='Submitted',
        )

        # Login as admin, and also simulate another student's reg_no in session
        session = self.client.session
        session['admin_user'] = 'admin'
        session['reg_no'] = 'OTHER_STUDENT_999'
        session.save()

        # Print slip should successfully open and return 200
        response = self.client.get(reverse('enrollment_print', kwargs={'enrollment_no': enrollment.enrollment_no}))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('Amit Verma', content)
        self.assertIn('CCP990001', content)

    def test_manage_enrollments_view_and_filters(self):
        from admissions.models import StudentEnrollment

        e1 = StudentEnrollment.objects.create(
            enrollment_no='CCP990002',
            reg_no='BSC001',
            student=self.student_bsc,
            full_name='Amit Verma',
            program_type='B.Sc. First Semester',
            is_submitted=True,
            status='Submitted',
        )
        e2 = StudentEnrollment.objects.create(
            enrollment_no='CCP990003',
            reg_no='BA001',
            student=self.student_ba,
            full_name='Priya Singh',
            program_type='B.A. First Semester',
            is_submitted=True,
            status='Approved',
        )

        self._login_admin()
        # View all
        resp = self.client.get(reverse('manage_enrollments'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['enrollments']), 2)
        content = resp.content.decode('utf-8')
        self.assertIn('Manage Student Enrollments', content)
        self.assertIn('Amit Verma', content)
        self.assertIn('Priya Singh', content)

        # Filter by program
        resp_prog = self.client.get(reverse('manage_enrollments') + '?program=B.Sc.+First+Semester')
        self.assertEqual(resp_prog.status_code, 200)
        self.assertEqual(len(resp_prog.context['enrollments']), 1)
        self.assertEqual(resp_prog.context['enrollments'][0].reg_no, 'BSC001')

        # Filter by status
        resp_status = self.client.get(reverse('manage_enrollments') + '?status=Approved')
        self.assertEqual(resp_status.status_code, 200)
        self.assertEqual(len(resp_status.context['enrollments']), 1)
        self.assertEqual(resp_status.context['enrollments'][0].reg_no, 'BA001')

    def test_admin_single_enrollment_approve_and_reset(self):
        from admissions.models import StudentEnrollment

        e = StudentEnrollment.objects.create(
            reg_no='BSC001',
            student=self.student_bsc,
            full_name='Amit Verma',
            program_type='B.Sc. First Semester',
            is_submitted=True,
            status='Submitted',
        )
        self.assertFalse(self.student_bsc.is_verified)
        self.assertIsNone(e.enrollment_no)

        self._login_admin()
        # Approve enrollment
        resp_approve = self.client.post(
            reverse('update_enrollment_status', kwargs={'pk': e.pk}),
            {'status': 'Approved'}
        )
        self.assertEqual(resp_approve.status_code, 302)

        e.refresh_from_db()
        self.assertEqual(e.status, 'Approved')
        self.assertTrue(e.is_submitted)
        self.assertIsNotNone(e.enrollment_no)  # Auto-generated on approval!
        self.student_bsc.refresh_from_db()
        self.assertTrue(self.student_bsc.is_verified)

        # Reset to Draft
        resp_draft = self.client.post(
            reverse('update_enrollment_status', kwargs={'pk': e.pk}),
            {'status': 'Draft'}
        )
        self.assertEqual(resp_draft.status_code, 302)
        e.refresh_from_db()
        self.assertEqual(e.status, 'Draft')
        self.assertFalse(e.is_submitted)

    def test_admin_bulk_approve_enrollments(self):
        from admissions.models import StudentEnrollment

        e1 = StudentEnrollment.objects.create(
            reg_no='BSC001',
            student=self.student_bsc,
            full_name='Amit Verma',
            program_type='B.Sc. First Semester',
            is_submitted=True,
            status='Submitted',
        )
        e2 = StudentEnrollment.objects.create(
            reg_no='BA001',
            student=self.student_ba,
            full_name='Priya Singh',
            program_type='B.A. First Semester',
            is_submitted=True,
            status='Submitted',
        )

        self._login_admin()
        # Bulk approve
        post_data = {
            'enrollment_ids': [e1.pk, e2.pk],
            'status': 'Approved',
        }
        resp = self.client.post(reverse('bulk_update_enrollment_status'), post_data)
        self.assertEqual(resp.status_code, 302)

        e1.refresh_from_db()
        e2.refresh_from_db()
        self.assertEqual(e1.status, 'Approved')
        self.assertEqual(e2.status, 'Approved')
        self.assertTrue(e1.is_submitted)
        self.assertTrue(e2.is_submitted)
        self.assertIsNotNone(e1.enrollment_no)
        self.assertIsNotNone(e2.enrollment_no)

        self.student_bsc.refresh_from_db()
        self.student_ba.refresh_from_db()
        self.assertTrue(self.student_bsc.is_verified)
        self.assertTrue(self.student_ba.is_verified)



