from django.contrib import admin
from .models import GrievanceCommitteeMember, GrievanceSubmission, CommitteeInfo


@admin.register(GrievanceCommitteeMember)
class GrievanceCommitteeMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'committee', 'designation', 'role_in_committee', 'order')
    list_filter = ('committee',)
    list_editable = ('order',)
    search_fields = ('name', 'designation')


@admin.register(GrievanceSubmission)
class GrievanceSubmissionAdmin(admin.ModelAdmin):
    list_display = ('complainant_name', 'grievance_type', 'subject', 'status', 'submitted_at')
    list_filter = ('grievance_type', 'status')
    list_editable = ('status',)
    search_fields = ('complainant_name', 'subject')
    readonly_fields = ('submitted_at',)
    fieldsets = (
        ('Complainant', {'fields': ('complainant_name', 'email', 'mobile', 'roll_number')}),
        ('Grievance', {'fields': ('grievance_type', 'subject', 'description', 'supporting_document')}),
        ('Resolution', {'fields': ('status', 'remarks')}),
        ('Meta', {'fields': ('submitted_at',)}),
    )


@admin.register(CommitteeInfo)
class CommitteeInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'committee')
