from django.db import models


class NAACDocument(models.Model):
    DOC_TYPE_CHOICES = [
        ('iiqa', 'IIQA'),
        ('ssr', 'SSR'),
        ('dvv', 'DVV'),
        ('atr', 'ATR'),
        ('naac', 'NAAC General'),
        ('aqar', 'AQAR'),
    ]
    doc_type = models.CharField(max_length=10, choices=DOC_TYPE_CHOICES)
    title = models.CharField(max_length=300)
    document = models.FileField(upload_to='naac/documents/', blank=True)
    document_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-uploaded_at']
        verbose_name = "NAAC Document"

    def __str__(self):
        return f"[{self.get_doc_type_display()}] {self.title}"

    def get_file(self):
        return self.document.url if self.document else self.document_url


class IQACMember(models.Model):
    ROLE_CHOICES = [
        ('chairman', 'Chairman'),
        ('coordinator', 'Coordinator'),
        ('member', 'Member'),
        ('external', 'External Member'),
    ]
    name = models.CharField(max_length=150)
    designation = models.CharField(max_length=200)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    department = models.CharField(max_length=150, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "IQAC Member"

    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"


class NAACCriteria(models.Model):
    CRITERION_CHOICES = [
        ('1', 'Criterion I'),
        ('2', 'Criterion II'),
        ('3', 'Criterion III'),
        ('4', 'Criterion IV'),
        ('5', 'Criterion V'),
        ('6', 'Criterion VI'),
        ('7', 'Criterion VII'),
    ]
    criterion = models.CharField(
        max_length=2,
        choices=CRITERION_CHOICES,
        default='1',
        verbose_name="Criterion"
    )
    criterion_number = models.CharField(max_length=10, verbose_name="Metric Number")
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    document = models.FileField(upload_to='naac/criteria/', blank=True)
    document_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'criterion_number']
        verbose_name = "NAAC Criteria"
        verbose_name_plural = "NAAC Criteria"

    def __str__(self):
        return f"Criterion {self.criterion_number}: {self.title}"


class NAACInfo(models.Model):
    """NAAC home page info"""
    grade = models.CharField(max_length=5, default="A")
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    accreditation_date = models.DateField(blank=True, null=True)
    valid_until = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    certificate_image = models.ImageField(upload_to='naac/', blank=True)

    class Meta:
        verbose_name = "NAAC Info"
        verbose_name_plural = "NAAC Info"

    def __str__(self):
        return f"NAAC Grade {self.grade}"
