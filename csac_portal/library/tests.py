from datetime import timedelta
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from library.models import (
    Book, BookCopy, StudentProfile, LibraryRequest, CirculationTransaction,
    LibrarySetting, Publisher, Subject
)
from library.services.circulation_service import (
    create_book_request, approve_book_request, reject_book_request,
    issue_physical_book, request_book_return, confirm_book_return,
    calculate_overdue_fine
)
from library.services.excel_import_service import validate_import_data, commit_import_records


class LibraryCirculationTests(TestCase):
    def setUp(self):
        # Settings
        self.settings = LibrarySetting.get_settings()
        self.settings.max_books_per_student = 2
        self.settings.default_loan_days = 14
        self.settings.fine_per_day = 2.00
        self.settings.max_pending_requests = 2
        self.settings.save()

        # Staff User
        self.staff_user = User.objects.create_user(
            username='librarian1',
            password='password123',
            is_staff=True
        )

        # Student User & Profile
        self.student_user = User.objects.create_user(
            username='student1',
            password='password123',
            first_name='Rahul',
            last_name='Sharma'
        )
        self.student_profile = StudentProfile.objects.create(
            user=self.student_user,
            enrollment_number='ENR-2026-001',
            library_card_number='CARD-001',
            course='B.Sc Computer Science',
            semester=5,
            mobile='9876543210',
            status='ACTIVE',
            is_library_eligible=True
        )

        # Book & Copies
        self.book = Book.objects.create(
            title='Database System Concepts',
            author='Abraham Silberschatz',
            isbn='9780073523323'
        )
        self.copy_1 = BookCopy.objects.create(
            book=self.book,
            accession_number='ACC-1001',
            rack_location='A-12',
            status='AVAILABLE'
        )
        self.copy_2 = BookCopy.objects.create(
            book=self.book,
            accession_number='ACC-1002',
            rack_location='A-12',
            status='AVAILABLE'
        )

    def test_book_request_lifecycle(self):
        """Test full request -> approve -> issue -> return-request -> return cycle."""
        # 1. Student requests copy 1
        req = create_book_request(self.student_profile, self.copy_1.id, remark="Exam prep")
        self.assertEqual(req.status, 'PENDING')
        self.copy_1.refresh_from_db()
        self.assertEqual(self.copy_1.status, 'REQUESTED')

        # 2. Prevent duplicate active request for same book
        with self.assertRaises(ValidationError):
            create_book_request(self.student_profile, self.copy_2.id)

        # 3. Librarian approves request (copy becomes RESERVED)
        req = approve_book_request(self.staff_user, req.id, expiry_days=3)
        self.assertEqual(req.status, 'APPROVED')
        self.copy_1.refresh_from_db()
        self.assertEqual(self.copy_1.status, 'RESERVED')

        # 4. Physical Book Issued at counter
        txn = issue_physical_book(self.staff_user, request_id=req.id)
        self.assertEqual(txn.status, 'ISSUED')
        self.copy_1.refresh_from_db()
        self.assertEqual(self.copy_1.status, 'ISSUED')
        self.assertEqual(self.student_profile.active_issued_count, 1)

        # 5. Student declares return
        txn = request_book_return(self.student_profile, txn.id)
        self.assertEqual(txn.status, 'RETURN_REQUESTED')
        self.copy_1.refresh_from_db()
        self.assertEqual(self.copy_1.status, 'RETURN_REQUESTED')

        # 6. Librarian confirms physical return
        txn = confirm_book_return(self.staff_user, txn.id, condition='GOOD')
        self.assertEqual(txn.status, 'RETURNED')
        self.copy_1.refresh_from_db()
        self.assertEqual(self.copy_1.status, 'AVAILABLE')
        self.assertEqual(self.student_profile.active_issued_count, 0)

    def test_borrowing_limit_enforcement(self):
        """Test student cannot exceed max_books_per_student limit."""
        # Issue 2 books to reach max quota of 2
        txn1 = issue_physical_book(self.staff_user, student_profile=self.student_profile, book_copy=self.copy_1)
        txn2 = issue_physical_book(self.staff_user, student_profile=self.student_profile, book_copy=self.copy_2)
        self.assertEqual(self.student_profile.active_issued_count, 2)

        # Create a 3rd copy
        copy_3 = BookCopy.objects.create(book=self.book, accession_number='ACC-1003', status='AVAILABLE')
        
        # 3rd request should fail quota check
        with self.assertRaises(ValidationError):
            create_book_request(self.student_profile, copy_3.id)

    def test_overdue_fine_calculation(self):
        """Test fine accrues correctly on overdue transactions."""
        # Issue copy with past due date (3 days ago)
        past_date = timezone.now().date() - timedelta(days=3)
        txn = CirculationTransaction.objects.create(
            student=self.student_profile,
            book_copy=self.copy_1,
            issued_by=self.staff_user,
            due_date=past_date,
            status='ISSUED'
        )

        fine_amt, days = calculate_overdue_fine(txn, self.settings)
        self.assertEqual(days, 3)
        self.assertEqual(fine_amt, 6.00) # 3 days * ₹2/day

        # Confirm return creates fine
        confirm_book_return(self.staff_user, txn.id, condition='GOOD')
        txn.refresh_from_db()
        self.assertEqual(txn.fine_amount, 6.00)
        self.assertEqual(self.student_profile.fines.count(), 1)

    def test_excel_import_service_validation(self):
        """Test excel import duplicate check and grouping."""
        sample_rows = [
            {'accession_number': 'ACC-1001', 'title': 'Existing Book', 'author': 'Author A', '_row_num': 2}, # Duplicate of setUp
            {'accession_number': 'ACC-2001', 'title': '', 'author': 'Author B', '_row_num': 3}, # Missing title
            {'accession_number': 'ACC-2002', 'title': 'New Book', 'author': 'Author C', 'rack_location': 'B-1', '_row_num': 4}, # Valid
            {'accession_number': 'ACC-2003', 'title': 'New Book', 'author': 'Author C', 'rack_location': 'B-1', '_row_num': 5}, # Valid copy 2 of same book
        ]

        val_res = validate_import_data(sample_rows)
        self.assertEqual(val_res['total_rows'], 4)
        self.assertEqual(val_res['error_count'], 2)
        self.assertEqual(val_res['valid_count'], 2)

        # Commit valid rows
        commit_res = commit_import_records(val_res['valid_rows'], uploaded_by_user=self.staff_user)
        self.assertEqual(commit_res['created_books'], 1) # Same book title
        self.assertEqual(commit_res['created_copies'], 2) # Two copies created
        self.assertTrue(BookCopy.objects.filter(accession_number='ACC-2002').exists())
        self.assertTrue(BookCopy.objects.filter(accession_number='ACC-2003').exists())
