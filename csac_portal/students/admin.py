from django.contrib import admin
from .models import (
    AdmissionInfo, OnlineAdmission, FeeStructure, Scholarship,
    AlumniProfile, MeritListEntry, LibraryResource, LibraryInfo, MeritListPageSettings,
    FeeStructurePageSettings
)


@admin.register(AdmissionInfo)
class AdmissionInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')


@admin.register(OnlineAdmission)
class OnlineAdmissionAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'program_applied', 'status', 'applied_at')
    list_filter = ('status', 'program_applied', 'category')
    search_fields = ('full_name', 'mobile', 'email')
    list_editable = ('status',)
    readonly_fields = ('applied_at',)
    fieldsets = (
        ('Personal Info', {'fields': ('full_name', 'father_name', 'mother_name', 'date_of_birth', 'gender', 'category')}),
        ('Contact', {'fields': ('mobile', 'email', 'address')}),
        ('Academic', {'fields': ('program_applied', 'last_exam_passed', 'last_exam_percentage')}),
        ('Documents', {'fields': ('photo', 'signature', 'marksheet')}),
        ('Status', {'fields': ('status',)}),
    )


@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('program', 'category', 'annual_fee', 'academic_year', 'order')
    list_filter = ('academic_year',)
    list_editable = ('order',)
    search_fields = ('program',)


@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'deadline', 'order')
    list_editable = ('order',)


@admin.register(AlumniProfile)
class AlumniProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'batch_year', 'program', 'current_position', 'is_featured')
    list_filter = ('batch_year', 'is_featured')
    list_editable = ('is_featured',)
    search_fields = ('name', 'current_position')


@admin.register(MeritListEntry)
class MeritListEntryAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'subject', 'medal_type', 'year', 'rank')
    list_filter = ('year', 'medal_type')
    search_fields = ('student_name', 'subject')


@admin.register(LibraryResource)
class LibraryResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'resource_type', 'subject')
    list_filter = ('resource_type', 'subject')
    search_fields = ('title', 'author')


@admin.register(LibraryInfo)
class LibraryInfoAdmin(admin.ModelAdmin):
    list_display = ('total_books', 'total_journals', 'total_digital', 'updated_at')


@admin.register(MeritListPageSettings)
class MeritListPageSettingsAdmin(admin.ModelAdmin):
    list_display = ('title', 'show_poster')
    list_editable = ('show_poster',)

    def has_add_permission(self, request):
        if MeritListPageSettings.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(FeeStructurePageSettings)
class FeeStructurePageSettingsAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')

    def has_add_permission(self, request):
        if FeeStructurePageSettings.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False


