from django.contrib import admin
from .models import (
    Department, DepartmentFaculty, DepartmentActivity, Program, ProgramType,
    COPOMapping, Syllabus, AcademicCalendar, DepartmentBanner, DepartmentLink,
)
from .forms import DepartmentFacultyForm, DepartmentForm, DepartmentBannerForm, ProgramForm, ProgramTypeForm


class DepartmentBannerInline(admin.TabularInline):
    model = DepartmentBanner
    form = DepartmentBannerForm
    extra = 1
    fields = ('image', 'caption', 'order')


class DepartmentFacultyInline(admin.TabularInline):
    model = DepartmentFaculty
    form = DepartmentFacultyForm
    extra = 1
    fields = ('name', 'designation', 'qualification', 'specialization', 'photo', 'order')


class DepartmentActivityInline(admin.TabularInline):
    model = DepartmentActivity
    extra = 1
    fields = ('title', 'description', 'image', 'date')


class DepartmentLinkInline(admin.TabularInline):
    model = DepartmentLink
    extra = 1
    fields = ('title', 'url', 'image', 'order')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    form = DepartmentForm
    list_display = ('name', 'category', 'hod_name', 'order')
    list_filter = ('category',)
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'hod_name')
    inlines = [DepartmentBannerInline, DepartmentFacultyInline, DepartmentActivityInline, DepartmentLinkInline]
    fieldsets = (
        ('Basic Info', {'fields': ('name', 'slug', 'category', 'established_year', 'external_links_heading', 'order')}),
        ('HOD', {'fields': ('hod_name', 'hod_photo', 'hod_message')}),
        ('Description', {'fields': ('description',)}),
        ('Banner', {'fields': ('banner_image', 'banner_image_url')}),
    )

    class Media:
        js = ('admin/js/department_admin.js',)



@admin.register(DepartmentFaculty)
class DepartmentFacultyAdmin(admin.ModelAdmin):
    form = DepartmentFacultyForm
    list_display = ('name', 'department', 'designation', 'order')
    list_filter = ('department',)
    search_fields = ('name', 'designation')
    list_editable = ('order',)



@admin.register(ProgramType)
class ProgramTypeAdmin(admin.ModelAdmin):
    form = ProgramTypeForm
    list_display = ('name', 'code', 'tab_label', 'icon_class', 'order', 'is_active', 'show_in_tab')
    list_editable = ('order', 'is_active', 'show_in_tab')
    list_filter = ('is_active', 'show_in_tab')
    search_fields = ('name', 'code', 'tab_label')
    prepopulated_fields = {'code': ('name',)}


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    form = ProgramForm
    list_display = ('name', 'program_type', 'department', 'duration', 'seats', 'introduced_year', 'order')
    list_filter = ('program_type', 'department')
    list_editable = ('order',)
    search_fields = ('name',)


@admin.register(COPOMapping)
class COPOMappingAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_name', 'department')
    list_filter = ('department',)
    search_fields = ('course_code', 'course_name')


@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'program', 'academic_year', 'is_nep_2020', 'order', 'uploaded_at')
    list_filter = ('is_nep_2020', 'department', 'academic_year')
    list_editable = ('is_nep_2020', 'order')
    search_fields = ('title',)


@admin.register(AcademicCalendar)
class AcademicCalendarAdmin(admin.ModelAdmin):
    list_display = ('title', 'academic_year', 'is_active')
    list_filter = ('academic_year', 'is_active')
    list_editable = ('is_active',)


@admin.register(DepartmentLink)
class DepartmentLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'url', 'order')
    list_filter = ('department',)
    list_editable = ('order',)
    search_fields = ('title', 'url')
