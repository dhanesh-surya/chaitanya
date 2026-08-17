from django.shortcuts import render, redirect
from django.contrib import messages
from .models import AdmissionInfo, FeeStructure, Scholarship, AlumniProfile, MeritListEntry, LibraryResource, LibraryInfo, MeritListPageSettings, FeeStructurePageSettings
from academics.models import Syllabus
from .forms import OnlineAdmissionForm


def admission(request):
    info = AdmissionInfo.objects.first()
    context = {
        'info': info,
        'page_title': 'Admission Procedure',
        'breadcrumb': 'Admission Procedure',
    }
    return render(request, 'students/admission.html', context)


def online_admission(request):
    if request.method == 'POST':
        form = OnlineAdmissionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your admission application has been submitted successfully! We will contact you soon.')
            return redirect('students:online_admission')
    else:
        form = OnlineAdmissionForm()
    context = {
        'form': form,
        'page_title': 'Online Admission',
        'breadcrumb': 'Online Admission Form',
    }
    return render(request, 'students/online_admission.html', context)


def fee_structure(request):
    fees = FeeStructure.objects.all()
    years = fees.values_list('academic_year', flat=True).distinct()
    fee_settings = FeeStructurePageSettings.objects.first()
    context = {
        'fees': fees,
        'years': years,
        'fee_settings': fee_settings,
        'page_title': 'Fee Structure',
        'breadcrumb': 'Tuition & Fee Structure',
    }
    return render(request, 'students/fee_structure.html', context)


def scholarship(request):
    scholarships = Scholarship.objects.all()
    context = {
        'scholarships': scholarships,
        'page_title': 'Scholarship',
        'breadcrumb': 'Scholarship Information',
    }
    return render(request, 'students/scholarship.html', context)


def alumni(request):
    featured = AlumniProfile.objects.filter(is_featured=True)
    all_alumni = AlumniProfile.objects.all()
    merit_list = MeritListEntry.objects.all().order_by('-year')
    context = {
        'featured': featured,
        'all_alumni': all_alumni,
        'merit_list': merit_list,
        'page_title': 'Alumni',
        'breadcrumb': 'Alumni',
    }
    return render(request, 'students/alumni.html', context)


def library(request):
    lib_info = LibraryInfo.objects.first()
    books = LibraryResource.objects.filter(resource_type='book')[:20]
    journals = LibraryResource.objects.filter(resource_type='journal')[:10]
    digital = LibraryResource.objects.filter(resource_type='digital')[:10]
    context = {
        'lib_info': lib_info,
        'books': books,
        'journals': journals,
        'digital': digital,
        'page_title': 'Library',
        'breadcrumb': 'Central Library',
    }
    return render(request, 'students/library.html', context)


def merit_list(request):
    merit = MeritListEntry.objects.all().order_by('-year')
    merit_settings = MeritListPageSettings.objects.first()
    context = {
        'merit_list': merit,
        'merit_settings': merit_settings,
        'page_title': 'Merit List',
        'breadcrumb': 'University Merit List',
    }
    return render(request, 'students/merit_list.html', context)


def syllabus(request):
    syllabi = Syllabus.objects.select_related('department', 'program').all()
    context = {
        'syllabi': syllabi,
        'page_title': 'Syllabus',
        'breadcrumb': 'Syllabus',
    }
    return render(request, 'students/syllabus.html', context)
