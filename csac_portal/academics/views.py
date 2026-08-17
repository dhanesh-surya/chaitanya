from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Department, Program, ProgramType, COPOMapping, AcademicCalendar, Syllabus


def _programs_for_type(program_type, programs_queryset):
    return programs_queryset.filter(
        Q(program_type=program_type.code) | Q(program_type=program_type.name)
    )


def department_detail(request, slug):
    dept = get_object_or_404(Department, slug=slug)
    faculty = dept.faculty.all()
    activities = dept.activities.all()[:6]
    programs = dept.programs.all()
    copo = dept.copo_mappings.all()
    syllabi = dept.syllabi.all()
    happenings = dept.happenings.all()
    context = {
        'dept': dept,
        'faculty': faculty,
        'activities': activities,
        'programs': programs,
        'copo': copo,
        'syllabi': syllabi,
        'happenings': happenings,
        'page_title': dept.name,
        'breadcrumb': f"Department of {dept.name}",
    }
    return render(request, 'academics/department_detail.html', context)


def programs(request):
    all_programs = Program.objects.select_related('department').order_by('order', 'name')
    program_types = ProgramType.objects.filter(is_active=True, show_in_tab=True).order_by('order', 'name')
    program_tab_sections = [
        {
            'program_type': program_type,
            'programs': _programs_for_type(program_type, all_programs),
        }
        for program_type in program_types
    ]
    departments = Department.objects.all()
    context = {
        'all_programs': all_programs,
        'program_types': program_types,
        'program_tab_sections': program_tab_sections,
        'departments': departments,
        'page_title': 'Programs Offered',
        'breadcrumb': 'Programs Offered',
    }
    return render(request, 'academics/programs.html', context)


def academic_calendar(request):
    calendars = AcademicCalendar.objects.filter(is_active=True)
    context = {
        'calendars': calendars,
        'page_title': 'Academic Calendar',
        'breadcrumb': 'Academic Calendar',
    }
    return render(request, 'academics/academic_calendar.html', context)
