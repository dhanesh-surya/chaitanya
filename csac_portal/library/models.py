import uuid
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from academics.models import Department


class Publisher(models.Model):
    name = models.CharField(max_length=200, unique=True)
    address = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class BookCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Book Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class StudentProfile(models.Model):
    STATUS_CHOICES = [
        ('PENDING_APPROVAL', 'Pending Approval'),
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('BLOCKED', 'Blocked'),
        ('REJECTED', 'Rejected'),
        ('GRADUATED', 'Graduated'),
        ('SUSPENDED', 'Suspended'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='library_student_profile')
    enrollment_number = models.CharField(max_length=50, unique=True, db_index=True)
    library_card_number = models.CharField(max_length=50, unique=True, db_index=True)
    father_mother_name = models.CharField(max_length=150, blank=True)
    course = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='library_students')
    semester = models.PositiveSmallIntegerField(default=1)
    academic_year = models.CharField(max_length=20, default='2026-2027')
    mobile = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='library/students/photos/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    is_library_eligible = models.BooleanField(default=True)
    registered_online = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_student_profiles')
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        name = self.user.get_full_name() or self.user.username
        return f"{name} ({self.enrollment_number})"

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username

    @property
    def active_issued_count(self):
        return self.circulation_records.filter(status='ISSUED').count()

    @property
    def pending_requests_count(self):
        return self.book_requests.filter(status__in=['PENDING', 'APPROVED']).count()

    @property
    def has_overdue(self):
        return self.circulation_records.filter(status='ISSUED', due_date__lt=timezone.now().date()).exists()

    @property
    def overdue_books(self):
        return self.circulation_records.filter(status='ISSUED', due_date__lt=timezone.now().date())


class LibrarianProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='library_staff_profile')
    employee_id = models.CharField(max_length=50, unique=True)
    designation = models.CharField(max_length=100, default='Librarian')
    contact_phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        name = self.user.get_full_name() or self.user.username
        return f"{name} [{self.employee_id}]"


class Book(models.Model):
    title = models.CharField(max_length=300, db_index=True)
    subtitle = models.CharField(max_length=300, blank=True)
    author = models.CharField(max_length=300, db_index=True)
    isbn = models.CharField(max_length=30, blank=True, db_index=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    edition = models.CharField(max_length=50, blank=True)
    publication_year = models.PositiveIntegerField(null=True, blank=True)
    language = models.CharField(max_length=50, default='English')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    category = models.ForeignKey(BookCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='library_books')
    volume = models.CharField(max_length=50, blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cover_image = models.ImageField(upload_to='library/covers/', blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['title', 'author']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.title} by {self.author}"

    @property
    def total_copies_count(self):
        return self.copies.filter(is_active=True).count()

    @property
    def available_copies_count(self):
        return self.copies.filter(is_active=True, status='AVAILABLE').count()

    @property
    def is_available(self):
        return self.available_copies_count > 0


class BookCopy(models.Model):
    COPY_STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('REQUESTED', 'Requested'),
        ('RESERVED', 'Reserved'),
        ('ISSUED', 'Issued'),
        ('RETURN_REQUESTED', 'Return Requested'),
        ('LOST', 'Lost'),
        ('DAMAGED', 'Damaged'),
        ('MAINTENANCE', 'Under Maintenance'),
        ('INACTIVE', 'Inactive'),
    ]

    CONDITION_CHOICES = [
        ('NEW', 'Brand New'),
        ('GOOD', 'Good Condition'),
        ('FAIR', 'Fair / Minor Wear'),
        ('DAMAGED', 'Damaged'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='copies')
    accession_number = models.CharField(max_length=100, unique=True, db_index=True)
    barcode = models.CharField(max_length=100, unique=True, null=True, blank=True)
    rack_location = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=25, choices=COPY_STATUS_CHOICES, default='AVAILABLE', db_index=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='GOOD')
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Book Copies"
        ordering = ['accession_number']

    def __str__(self):
        return f"{self.book.title} [Acc: {self.accession_number}] ({self.get_status_display()})"

    @property
    def student_status_label(self):
        if self.status == 'AVAILABLE':
            return 'Available'
        elif self.status == 'ISSUED':
            return 'Issued'
        elif self.status in ['REQUESTED', 'RESERVED']:
            return 'Request Pending'
        else:
            return 'Unavailable'

    @property
    def badge_class(self):
        if self.status == 'AVAILABLE':
            return 'bg-success'
        elif self.status == 'ISSUED':
            return 'bg-danger'
        elif self.status in ['REQUESTED', 'RESERVED']:
            return 'bg-warning text-dark'
        else:
            return 'bg-secondary'


class LibraryRequest(models.Model):
    REQUEST_STATUS = [
        ('PENDING', 'Pending Review'),
        ('APPROVED', 'Approved (Awaiting Collection)'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled by Student'),
        ('ISSUED', 'Fulfilled / Issued'),
        ('EXPIRED', 'Expired'),
    ]

    request_number = models.CharField(max_length=50, unique=True, editable=False)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='book_requests')
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE, related_name='requests')
    student_remark = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=REQUEST_STATUS, default='PENDING', db_index=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_library_requests')
    rejection_reason = models.TextField(blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-requested_at']

    def save(self, *args, **kwargs):
        if not self.request_number:
            self.request_number = f"LIB-REQ-{timezone.now().strftime('%y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.request_number} - {self.student.enrollment_number} ({self.status})"


class CirculationTransaction(models.Model):
    TRANSACTION_STATUS = [
        ('ISSUED', 'Currently Issued'),
        ('RETURN_REQUESTED', 'Return Initiated by Student'),
        ('RETURNED', 'Successfully Returned'),
        ('LOST', 'Reported Lost'),
        ('DAMAGED', 'Reported Damaged'),
    ]

    transaction_number = models.CharField(max_length=50, unique=True, editable=False)
    request = models.OneToOneField(LibraryRequest, on_delete=models.SET_NULL, null=True, blank=True, related_name='circulation')
    student = models.ForeignKey(StudentProfile, on_delete=models.PROTECT, related_name='circulation_records')
    book_copy = models.ForeignKey(BookCopy, on_delete=models.PROTECT, related_name='circulation_history')
    
    issued_at = models.DateTimeField(default=timezone.now)
    issued_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='issued_library_transactions')
    due_date = models.DateField(db_index=True)
    
    return_requested_at = models.DateTimeField(null=True, blank=True)
    return_request_remark = models.CharField(max_length=255, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    returned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_library_returns')
    
    status = models.CharField(max_length=25, choices=TRANSACTION_STATUS, default='ISSUED', db_index=True)
    condition_at_issue = models.CharField(max_length=20, default='GOOD')
    condition_at_return = models.CharField(max_length=20, blank=True)
    
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    fine_paid = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ['-issued_at']

    def save(self, *args, **kwargs):
        if not self.transaction_number:
            self.transaction_number = f"TXN-{timezone.now().strftime('%y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_number} - {self.book_copy.accession_number} to {self.student.enrollment_number}"

    @property
    def is_overdue(self):
        if self.status in ['ISSUED', 'RETURN_REQUESTED']:
            return timezone.now().date() > self.due_date
        return False

    @property
    def overdue_days(self):
        if self.is_overdue:
            return (timezone.now().date() - self.due_date).days
        return 0


class Fine(models.Model):
    transaction = models.ForeignKey(CirculationTransaction, on_delete=models.CASCADE, related_name='fines')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='fines')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    overdue_days = models.PositiveIntegerField(default=0)
    is_settled = models.BooleanField(default=False)
    settled_at = models.DateTimeField(null=True, blank=True)
    settled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='settled_fines')
    payment_method = models.CharField(max_length=50, blank=True) # Cash, Online, Waived
    remarks = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Fine: ₹{self.amount} for {self.student.enrollment_number}"


class LibrarySetting(models.Model):
    max_books_per_student = models.PositiveIntegerField(default=3, help_text="Maximum concurrent issued books allowed")
    default_loan_days = models.PositiveIntegerField(default=14, help_text="Default borrowing period in days")
    fine_per_day = models.DecimalField(max_digits=5, decimal_places=2, default=2.00, help_text="Fine charged per overdue day (₹)")
    max_renewals = models.PositiveIntegerField(default=1)
    max_pending_requests = models.PositiveIntegerField(default=2, help_text="Maximum active requests a student can have pending")
    request_expiry_days = models.PositiveIntegerField(default=3, help_text="Days an approved reservation is held before returning to shelf")
    allow_borrowing_if_fines = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Library Setting"
        verbose_name_plural = "Library Settings"

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj

    def __str__(self):
        return f"Library Configuration (Max {self.max_books_per_student} books, {self.default_loan_days} days loan)"


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('BOOK_CREATED', 'Book Created'),
        ('BOOK_EDITED', 'Book Edited'),
        ('BOOK_IMPORTED', 'Book Imported from Excel'),
        ('REQUEST_CREATED', 'Book Request Created'),
        ('REQUEST_APPROVED', 'Request Approved'),
        ('REQUEST_REJECTED', 'Request Rejected'),
        ('REQUEST_CANCELLED', 'Request Cancelled'),
        ('BOOK_ISSUED', 'Physical Book Issued'),
        ('RETURN_REQUESTED', 'Return Requested'),
        ('RETURN_CONFIRMED', 'Return Confirmed'),
        ('STATUS_CHANGED', 'Copy Status Changed'),
        ('STUDENT_CREATED', 'Student Account Created'),
        ('STUDENT_REGISTERED', 'Student Self-Registered'),
        ('STUDENT_APPROVED', 'Student Registration Approved'),
        ('STUDENT_REJECTED', 'Student Registration Rejected'),
        ('STUDENT_PASSWORD_RESET', 'Student Password Reset'),
        ('STUDENT_BLOCKED', 'Student Blocked'),
        ('FINE_SETTLED', 'Fine Settled'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='library_audit_logs')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    reference_id = models.CharField(max_length=100)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M')} - {self.action} ({self.reference_id})"


class ExcelImport(models.Model):
    file_name = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='library_excel_imports')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    total_rows = models.PositiveIntegerField(default=0)
    valid_rows = models.PositiveIntegerField(default=0)
    duplicate_accessions = models.PositiveIntegerField(default=0)
    missing_fields = models.PositiveIntegerField(default=0)
    error_log = models.TextField(blank=True)
    status = models.CharField(max_length=30, default='PENDING')

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Import {self.file_name} ({self.status}) on {self.uploaded_at.strftime('%Y-%m-%d')}"
