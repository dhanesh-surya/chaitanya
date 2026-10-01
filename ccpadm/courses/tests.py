from django.core.management import call_command
from django.test import TestCase
from courses.models import Program, ProgramCourse


class ProgramCourseFieldsTestCase(TestCase):
    def test_program_course_curriculum_fields(self):
        course = ProgramCourse.objects.create(
            program_type='B.A.',
            department='Hindi',
            course_name='Hindi Sahitya Ka Itihas',
            course_code='HNSC-01',
            semester='I',
            paper_no='I',
            course_type_1='Theory',
            course_type_2='DSC',
            credit_l='4',
            credit_t='1',
            credit_p='0',
        )
        self.assertEqual(course.course_code, 'HNSC-01')
        self.assertEqual(course.semester, 'I')
        self.assertEqual(course.paper_no, 'I')
        self.assertEqual(course.credit_l, '4')


class SeedNepCoursesTestCase(TestCase):
    def test_seed_nep_courses_populates_curriculum(self):
        call_command('seed_nep_courses')
        # Check BA courses
        ba_hindi = ProgramCourse.objects.filter(program_type='B.A.', course_code='HNSC-01').first()
        self.assertIsNotNone(ba_hindi)
        self.assertEqual(ba_hindi.course_type_2, 'DSC')

        # Check BCA courses
        bca_ds = ProgramCourse.objects.filter(program_type='BCA', course_code='CASC-01').first()
        self.assertIsNotNone(bca_ds)

        # Check auto select linkage (theory -> practical)
        bca_comp = ProgramCourse.objects.filter(program_type='BCA', course_code='CASC- 02T').first()
        self.assertIsNotNone(bca_comp)
        self.assertIsNotNone(bca_comp.auto_select_course)
        self.assertEqual(bca_comp.auto_select_course.course_code, 'CASC- 02P')


class ManageCoursesProgramFilterTestCase(TestCase):
    def setUp(self):
        self.course_ba = ProgramCourse.objects.create(
            program_type='B.A. First Semester',
            department='Hindi',
            course_name='Hindi Literature',
            course_type_1='Theory',
            course_type_2='DSC',
        )
        self.course_bsc = ProgramCourse.objects.create(
            program_type='B.Sc. First Semester',
            department='Chemistry',
            course_name='Inorganic Chemistry',
            course_type_1='Theory',
            course_type_2='DSC',
        )

    def _login_admin(self):
        session = self.client.session
        session['admin_user'] = 'admin'
        session.save()

    def test_default_courses_page_is_blank_and_prompts_to_select_program(self):
        self._login_admin()
        from django.urls import reverse

        response = self.client.get(reverse('manage_courses'))
        self.assertEqual(response.status_code, 200)

        # By default, 0 courses loaded
        self.assertEqual(len(response.context['courses']), 0)
        self.assertEqual(response.context['total_count'], 0)
        self.assertEqual(response.context['program_filter'], '')

        content = response.content.decode('utf-8')
        # "All Programs" must be removed
        self.assertNotIn('All Programs', content)
        # "-- Select Program --" option should be present
        self.assertIn('-- Select Program --', content)
        # Empty state message indicating no program selected
        self.assertIn('No Program Selected', content)
        self.assertIn('Please select a program from the dropdown above to see courses.', content)

    def test_courses_load_when_program_selected(self):
        self._login_admin()
        from django.urls import reverse

        response = self.client.get(reverse('manage_courses') + '?program=B.A.+First+Semester')
        self.assertEqual(response.status_code, 200)

        # Only B.A. courses loaded
        self.assertEqual(len(response.context['courses']), 1)
        self.assertEqual(response.context['courses'][0].course_name, 'Hindi Literature')
        self.assertEqual(response.context['total_count'], 1)

        content = response.content.decode('utf-8')
        self.assertIn('Hindi Literature', content)
        self.assertNotIn('Inorganic Chemistry', content)

    def test_edit_course_with_code_and_paper(self):
        self._login_admin()
        from django.urls import reverse

        # Edit course_ba to set course_code and paper_no
        post_data = {
            'program_type': 'B.A. First Semester',
            'department': 'Hindi',
            'course_name': 'Hindi Sahitya Ka Itihas',
            'course_code': 'HNSC-01',
            'paper_no': 'I',
            'course_type_1': 'Theory',
            'course_type_2': 'DSC',
            'is_compulsory': 'on',
        }
        response = self.client.post(reverse('edit_course', kwargs={'pk': self.course_ba.pk}), post_data)
        self.assertEqual(response.status_code, 302)

        self.course_ba.refresh_from_db()
        self.assertEqual(self.course_ba.course_code, 'HNSC-01')
        self.assertEqual(self.course_ba.paper_no, 'I')
        self.assertTrue(self.course_ba.is_compulsory)

        # GET manage_courses with edit parameter displays the course_code in the edit form and table
        resp = self.client.get(reverse('manage_courses') + f'?edit={self.course_ba.pk}&program=B.A.+First+Semester')
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode('utf-8')
        self.assertIn('HNSC-01', content)
        self.assertIn('value="HNSC-01"', content)
        self.assertIn('value="I"', content)
