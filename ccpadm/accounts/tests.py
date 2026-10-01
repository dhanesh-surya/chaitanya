from datetime import date
from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import Student
from admissions.models import StudentAdmission, StudentEnrollment


class ForgotPasswordTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('forgot_password')

        # Create sample student 1: Two-word name
        self.student1 = Student.objects.create(
            registration_no='AS26090001',
            full_name='Amar Kumar',
            aadhaar='653623072740',
            password='secret_pass_123',
            email='amar@example.com',
            mobile='9876543210',
            program_type='B.Sc. First Semester',
        )
        self.admission1 = StudentAdmission.objects.create(
            reg_no='AS26090001',
            full_name='Amar Kumar',
            dob=date(1995, 8, 15),
            aadhaar='653623072740',
        )

        # Create sample student 2: Single-word name
        self.student2 = Student.objects.create(
            registration_no='AS26090002',
            full_name='DHANANJAY',
            aadhaar='123456789012',
            password='pass_single_name',
            email='dhananjay@example.com',
            mobile='9876543211',
            program_type='B.A. First Semester',
        )
        self.admission2 = StudentAdmission.objects.create(
            reg_no='AS26090002',
            full_name='DHANANJAY',
            dob=date(2001, 3, 20),
            aadhaar='123456789012',
        )

        # Create sample student 3: Three-word name
        self.student3 = Student.objects.create(
            registration_no='AS26090003',
            full_name='Sonam Singh Barman',
            aadhaar='987654321098',
            password='sonam_pass_789',
            email='sonam@example.com',
            mobile='9876543212',
            program_type='B.Com. First Semester',
        )
        self.admission3 = StudentAdmission.objects.create(
            reg_no='AS26090003',
            full_name='Sonam Singh Barman',
            dob=date(2002, 11, 5),
            aadhaar='987654321098',
        )

    def test_get_forgot_password_page(self):
        """GET request should render the verification form."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/forgot_password.html')
        self.assertContains(response, 'Enter your Full Name')
        self.assertContains(response, 'Date of Birth')
        self.assertContains(response, 'Aadhaar Number')

    def test_successful_password_retrieval(self):
        """Valid Full Name, DOB, and Aadhaar should reveal the password."""
        response = self.client.post(self.url, {
            'full_name': 'Amar Kumar',
            'dob': '1995-08-15',
            'aadhaar': '6536 2307 2740',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['success'])
        self.assertEqual(response.context['matched_student'], self.student1)
        self.assertContains(response, 'secret_pass_123')
        self.assertContains(response, 'AS26090001')
        self.assertContains(response, 'Amar Kumar')

    def test_single_name_retrieval(self):
        """Single name student matching full_name."""
        response = self.client.post(self.url, {
            'full_name': 'Dhananjay',
            'dob': '2001-03-20',
            'aadhaar': '123456789012',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['success'])
        self.assertEqual(response.context['matched_student'], self.student2)
        self.assertContains(response, 'pass_single_name')

    def test_multi_token_name_retrieval(self):
        """Three-word name student (Sonam Singh Barman) entering first and last name as full name."""
        response = self.client.post(self.url, {
            'full_name': 'Sonam Barman',
            'dob': '2002-11-05',
            'aadhaar': '9876-5432-1098',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['success'])
        self.assertEqual(response.context['matched_student'], self.student3)
        self.assertContains(response, 'sonam_pass_789')

    def test_reversed_name_retrieval(self):
        """Reversed name (Kumar Amar instead of Amar Kumar) should still match."""
        response = self.client.post(self.url, {
            'full_name': 'Kumar Amar',
            'dob': '1995-08-15',
            'aadhaar': '653623072740',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['success'])
        self.assertEqual(response.context['matched_student'], self.student1)
        self.assertContains(response, 'secret_pass_123')

    def test_wrong_dob_failure(self):
        """Incorrect DOB should show error and not reveal password."""
        response = self.client.post(self.url, {
            'full_name': 'Amar Kumar',
            'dob': '1990-01-01',
            'aadhaar': '6536 2307 2740',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['success'])
        self.assertIsNone(response.context['matched_student'])
        self.assertNotContains(response, 'secret_pass_123')
        self.assertContains(response, 'The details provided do not match our records')

    def test_wrong_aadhaar_failure(self):
        """Incorrect Aadhaar should show error."""
        response = self.client.post(self.url, {
            'full_name': 'Amar Kumar',
            'dob': '1995-08-15',
            'aadhaar': '0000 0000 0000',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['success'])
        self.assertIsNone(response.context['matched_student'])
        self.assertContains(response, 'No student record found matching the provided Aadhaar Number')

    def test_wrong_name_failure(self):
        """Incorrect name should show error."""
        response = self.client.post(self.url, {
            'full_name': 'Vikram Sharma',
            'dob': '1995-08-15',
            'aadhaar': '6536 2307 2740',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['success'])
        self.assertIsNone(response.context['matched_student'])
        self.assertNotContains(response, 'secret_pass_123')
        self.assertContains(response, 'The details provided do not match our records')

    def test_invalid_aadhaar_length(self):
        """Aadhaar with fewer than 12 digits should be rejected."""
        response = self.client.post(self.url, {
            'full_name': 'Amar Kumar',
            'dob': '1995-08-15',
            'aadhaar': '12345',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['success'])
        self.assertContains(response, 'Please enter a valid 12-digit Aadhaar Number')
