from django.db import models


class GrievanceCommitteeMember(models.Model):
    COMMITTEE_CHOICES = [
        ('anti_ragging', 'Anti-Ragging Committee'),
        ('icc', 'Internal Complaints Committee (ICC)'),
        ('redressal', 'Grievance Redressal Committee'),
    ]
    committee = models.CharField(max_length=20, choices=COMMITTEE_CHOICES)
    name = models.CharField(max_length=150)
    designation = models.CharField(max_length=200)
    role_in_committee = models.CharField(max_length=100, blank=True, help_text="e.g. Chairman, Member, Convenor")
    department = models.CharField(max_length=150, blank=True)
    contact = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['committee', 'order']
        verbose_name = "Committee Member"

    def __str__(self):
        return f"{self.name} - {self.get_committee_display()}"


class GrievanceSubmission(models.Model):
    COMMITTEE_CHOICES = [
        ('anti_ragging', 'Anti-Ragging'),
        ('icc', 'Internal Complaints (ICC)'),
        ('redressal', 'General Grievance'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    grievance_type = models.CharField(max_length=20, choices=COMMITTEE_CHOICES)
    complainant_name = models.CharField(max_length=150)
    email = models.EmailField()
    mobile = models.CharField(max_length=15, blank=True)
    roll_number = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=300)
    description = models.TextField()
    supporting_document = models.FileField(upload_to='grievances/docs/', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    submitted_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, help_text="Admin remarks / resolution notes")

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Grievance Submission"

    def __str__(self):
        return f"{self.complainant_name} - {self.subject[:60]}"


class CommitteeInfo(models.Model):
    COMMITTEE_CHOICES = [
        ('anti_ragging', 'Anti-Ragging Committee'),
        ('icc', 'Internal Complaints Committee (ICC)'),
        ('redressal', 'Grievance Redressal Committee'),
    ]
    committee = models.CharField(max_length=20, choices=COMMITTEE_CHOICES, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    objectives = models.TextField(blank=True)
    document = models.FileField(upload_to='grievances/docs/', blank=True)

    class Meta:
        verbose_name = "Committee Info"
        verbose_name_plural = "Committees Info"

    def __str__(self):
        return self.title
