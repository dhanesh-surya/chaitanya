from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class AdmissionInfo(models.Model):
    title = models.CharField(max_length=200, default="Admission Procedure")
    content = models.TextField()
    important_dates = models.TextField(blank=True)
    documents_required = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Admission Info"
        verbose_name_plural = "Admission Info"

    def __str__(self):
        return self.title


class OnlineAdmission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    full_name = models.CharField(max_length=150)
    father_name = models.CharField(max_length=150)
    mother_name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    category = models.CharField(max_length=10, choices=[
        ('GEN', 'General'), ('OBC', 'OBC'), ('SC', 'SC'), ('ST', 'ST')
    ])
    mobile = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField()
    program_applied = models.CharField(max_length=200)
    last_exam_passed = models.CharField(max_length=100)
    last_exam_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    photo = models.ImageField(upload_to='admissions/photos/', blank=True)
    signature = models.ImageField(upload_to='admissions/signatures/', blank=True)
    marksheet = models.FileField(upload_to='admissions/docs/', blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-applied_at']
        verbose_name = "Online Admission Application"

    def __str__(self):
        return f"{self.full_name} - {self.program_applied}"


class FeeStructure(models.Model):
    program = models.CharField(max_length=200)
    category = models.CharField(max_length=50, blank=True)
    annual_fee = models.DecimalField(max_digits=10, decimal_places=2)
    admission_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    exam_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    academic_year = models.CharField(max_length=10, default="2024-25")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'program']
        verbose_name = "Fee Structure"

    def __str__(self):
        return f"{self.program} ({self.academic_year})"

    def total(self):
        return self.annual_fee + self.admission_fee + self.exam_fee + self.other_fee


class Scholarship(models.Model):
    name = models.CharField(max_length=200)
    eligibility = models.TextField()
    amount = models.CharField(max_length=100)
    deadline = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class AlumniProfile(models.Model):
    name = models.CharField(max_length=150)
    batch_year = models.IntegerField()
    program = models.CharField(max_length=200, blank=True)
    current_position = models.CharField(max_length=200, blank=True)
    organization = models.CharField(max_length=200, blank=True)
    achievement = models.TextField(blank=True)
    photo = models.ImageField(upload_to='alumni/', blank=True)
    testimonial = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-batch_year', 'name']

    def __str__(self):
        return f"{self.name} ({self.batch_year})"


class MeritListEntry(models.Model):
    student_name = models.CharField(max_length=150)
    subject = models.CharField(max_length=200)
    medal_type = models.CharField(max_length=50, choices=[
        ('gold', 'Gold Medal'), ('silver', 'Silver Medal'), ('bronze', 'Bronze Medal'), ('rank', 'University Rank')
    ])
    year = models.IntegerField()
    rank = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['-year', 'student_name']
        verbose_name = "Merit List Entry"

    def __str__(self):
        return f"{self.student_name} - {self.medal_type} ({self.year})"


class LibraryResource(models.Model):
    TYPE_CHOICES = [
        ('book', 'Book'),
        ('journal', 'Journal'),
        ('digital', 'Digital Resource'),
        ('thesis', 'Thesis'),
        ('magazine', 'Magazine'),
    ]
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=200, blank=True)
    resource_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    isbn = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=150, blank=True)
    link = models.URLField(blank=True)
    added_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['title']
        verbose_name = "Library Resource"

    def __str__(self):
        return self.title


class LibraryInfo(models.Model):
    """Library general info page content"""
    total_books = models.IntegerField(default=0)
    total_journals = models.IntegerField(default=0)
    total_digital = models.IntegerField(default=0)
    timing = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Library Info"
        verbose_name_plural = "Library Info"

    def __str__(self):
        return "Library Information"


class MeritListPageSettings(models.Model):
    title = models.CharField(max_length=200, default="University Merit List Settings")
    show_poster = models.BooleanField(default=True, verbose_name="Show Merit List Image", help_text="Toggle to hide or show the merit list poster/image on the page")
    poster_image = models.ImageField(upload_to='merit_list/', blank=True, null=True, verbose_name="Merit List Poster Image")
    poster_image_url = models.URLField(blank=True, verbose_name="Poster Image URL (External)", help_text="Use this for external URLs if no local image is uploaded")

    class Meta:
        verbose_name = "Merit List Page Settings"
        verbose_name_plural = "Merit List Page Settings"

    def __str__(self):
        return self.title

    def get_poster_image(self):
        if self.poster_image:
            return self.poster_image.url
        return self.poster_image_url


class FeeStructurePageSettings(models.Model):
    title = models.CharField(max_length=200, default="Fee Structure Page Settings")
    description = CKEditor5Field('Description', config_name='extends', blank=True, help_text="Rich text description/notes about the fee structure")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Fee Structure Page Settings"
        verbose_name_plural = "Fee Structure Page Settings"

    def __str__(self):
        return self.title


