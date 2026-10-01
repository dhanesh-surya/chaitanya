from django.contrib import admin, messages
from django.utils.html import strip_tags

from .forms import AdmissionSubmitInstructionForm, EnrollmentInstructionForm
from .models import (
    AdmissionSubmitInstruction,
    EnrollmentInstruction,
    StudentAdmission,
    StudentDocument,
    StudentEducation,
    StudentEnrollment,
)


@admin.register(StudentAdmission)
class StudentAdmissionAdmin(admin.ModelAdmin):
    list_display = ('application_no', 'reg_no', 'full_name', 'status', 'submitted_date')
    list_filter = ('status', 'program_type')
    search_fields = ('application_no', 'reg_no', 'full_name', 'email')


@admin.register(StudentEnrollment)
class StudentEnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        'enrollment_no',
        'reg_no',
        'full_name',
        'program_type',
        'semester',
        'status',
        'is_submitted',
        'submitted_date',
    )
    list_filter = ('status', 'is_submitted', 'program_type', 'semester')
    search_fields = ('enrollment_no', 'reg_no', 'full_name', 'email', 'mobile')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['approve_enrollment', 'reset_to_draft']

    @admin.action(description='Accept / Approve selected enrollment applications')
    def approve_enrollment(self, request, queryset):
        updated = queryset.update(status='Approved', is_submitted=True)
        self.message_user(
            request,
            f'{updated} enrollment application(s) marked as Approved / Accepted.',
            messages.SUCCESS,
        )

    @admin.action(description='Reset selected enrollments to Draft (Allow student to edit)')
    def reset_to_draft(self, request, queryset):
        updated = queryset.update(status='Draft', is_submitted=False)
        self.message_user(
            request,
            f'{updated} enrollment application(s) reset to Draft.',
            messages.SUCCESS,
        )


@admin.register(AdmissionSubmitInstruction)
class AdmissionSubmitInstructionAdmin(admin.ModelAdmin):
    form = AdmissionSubmitInstructionForm
    list_display = (
        'heading',
        'notice_preview',
        'sort_order',
        'is_active',
        'updated_at',
    )
    list_filter = ('is_active',)
    search_fields = ('heading', 'notice')
    ordering = ('sort_order', 'id')
    fieldsets = (
        (None, {
            'fields': ('is_active', 'sort_order'),
        }),
        ('Submit popup', {
            'fields': ('heading', 'notice'),
            'description': (
                'This content appears in a popup when a student clicks '
                '"Submit Application" on the admission preview page.'
            ),
        }),
    )

    @admin.display(description='Notice preview')
    def notice_preview(self, obj):
        text = strip_tags(obj.notice or '').strip().replace('\n', ' ')
        if len(text) > 80:
            return f'{text[:80]}…'
        return text or '—'


@admin.register(EnrollmentInstruction)
class EnrollmentInstructionAdmin(admin.ModelAdmin):
    form = EnrollmentInstructionForm
    list_display = (
        'title',
        'college_title',
        'is_active',
        'updated_at',
    )
    list_filter = ('is_active',)
    search_fields = ('title', 'college_title', 'content_html')
    fieldsets = (
        ('Display Status', {
            'fields': ('is_active',),
            'description': 'Toggle whether this instruction popup appears on student dashboards.',
        }),
        ('Popup Headers', {
            'fields': ('college_title', 'title'),
            'description': 'College and process headings shown at the top of the modal popup.',
        }),
        ('Step-by-Step Instructions', {
            'fields': ('content_html',),
            'description': 'Full instructions text shown to students upon logging into their dashboard.',
        }),
    )


admin.site.register(StudentEducation)
admin.site.register(StudentDocument)