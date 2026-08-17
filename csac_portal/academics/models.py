from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class Department(models.Model):
    CATEGORY_CHOICES = [
        ('arts', 'Arts'),
        ('science', 'Science'),
        ('commerce', 'Commerce & Management'),
    ]
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    hod_name = models.CharField(max_length=150, blank=True)
    hod_photo = models.ImageField(upload_to='dept/hod/', blank=True)
    hod_message = models.TextField(blank=True)
    description = CKEditor5Field('Description', config_name='extends', blank=True)
    banner_image = models.ImageField(upload_to='dept/banner/', blank=True)
    banner_image_url = models.URLField(blank=True)
    established_year = models.IntegerField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_image(self):
        return self.banner_image.url if self.banner_image else self.banner_image_url


class DepartmentBanner(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='banners')
    image = models.ImageField(upload_to='dept/banner/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Department Banner"
        verbose_name_plural = "Department Banners"

    def __str__(self):
        return f"Banner {self.id} for {self.department.name}"


class DepartmentFaculty(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='faculty')
    name = models.CharField(max_length=150)
    designation = models.CharField(max_length=200)
    qualification = models.CharField(max_length=300, blank=True)
    specialization = models.CharField(max_length=300, blank=True)
    photo = models.ImageField(upload_to='dept/faculty/', blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Department Faculty"
        verbose_name_plural = "Department Faculty"

    def __str__(self):
        return f"{self.name} ({self.department.name})"


class DepartmentActivity(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=300)
    description = CKEditor5Field('Description', config_name='extends', blank=True)
    image = models.ImageField(upload_to='dept/activities/', blank=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title


class ProgramType(models.Model):
    code = models.SlugField(
        max_length=30,
        unique=True,
        help_text="Short code stored on programs, e.g. ug, pg, diploma",
    )
    name = models.CharField(max_length=100, help_text="Label shown in admin when selecting a program type")
    tab_label = models.CharField(max_length=120, help_text="Label shown on the programs page tab")
    icon_class = models.CharField(
        max_length=80,
        default='fas fa-book',
        help_text="Font Awesome icon class for the programs page tab",
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    show_in_tab = models.BooleanField(
        default=True,
        help_text="Show this type as a separate tab on the programs page",
    )

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Program Type'
        verbose_name_plural = 'Program Types'

    def __str__(self):
        return self.name


class Program(models.Model):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='programs')
    name = models.CharField(max_length=200)
    program_type = models.CharField(max_length=30, help_text="Program type code from Program Types")
    duration = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g. 3 Years, 4 Semesters, 2 Years",
    )
    eligibility = models.TextField(blank=True)
    seats = models.CharField(max_length=50, default='0', verbose_name='Total Seats')
    introduced_year = models.IntegerField(blank=True, null=True)
    affiliation_status = models.CharField(max_length=100, blank=True)
    fee_per_year = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        type_label = self.get_program_type_label()
        return f"{self.name} ({type_label})" if type_label else self.name

    def get_program_type_label(self):
        program_type = ProgramType.objects.filter(code=self.program_type, is_active=True).first()
        return program_type.name if program_type else self.program_type


class COPOMapping(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='copo_mappings')
    course_code = models.CharField(max_length=20)
    course_name = models.CharField(max_length=200)
    program_outcomes = models.TextField(help_text="Store as formatted text or comma-separated PO codes")
    course_outcomes = models.TextField(help_text="List course outcomes")
    mapping_matrix = models.TextField(blank=True, help_text="CO-PO mapping table as text")

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"


class Syllabus(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='syllabi')
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    document = models.FileField(upload_to='syllabus/', blank=True)
    document_url = models.URLField(blank=True, help_text="External URL for the syllabus document (used if no local file is uploaded)")
    academic_year = models.CharField(max_length=10, blank=True)
    order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-uploaded_at']
        verbose_name_plural = "Syllabi"

    def __str__(self):
        return self.title

    def get_document(self):
        """Return local file URL if uploaded, otherwise the external URL."""
        if self.document:
            return self.document.url
        return self.document_url


class AcademicCalendar(models.Model):
    title = models.CharField(max_length=200)
    document = models.FileField(upload_to='academic_calendar/', blank=True)
    document_url = models.URLField(blank=True)
    academic_year = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-academic_year']

    def __str__(self):
        return f"{self.title} ({self.academic_year})"
