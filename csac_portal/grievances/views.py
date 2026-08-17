from django.shortcuts import render, redirect
from django.contrib import messages
from .models import GrievanceCommitteeMember, CommitteeInfo
from .forms import GrievanceForm


def anti_ragging(request):
    members = GrievanceCommitteeMember.objects.filter(committee='anti_ragging')
    info = CommitteeInfo.objects.filter(committee='anti_ragging').first()
    context = {
        'members': members,
        'info': info,
        'page_title': 'Anti-Ragging Committee',
        'breadcrumb': 'Anti-Ragging Committee',
    }
    return render(request, 'grievances/anti_ragging.html', context)


def icc(request):
    members = GrievanceCommitteeMember.objects.filter(committee='icc')
    info = CommitteeInfo.objects.filter(committee='icc').first()
    context = {
        'members': members,
        'info': info,
        'page_title': 'Internal Complaints Committee (ICC)',
        'breadcrumb': 'Internal Complaints Committee',
    }
    return render(request, 'grievances/icc.html', context)


def redressal(request):
    members = GrievanceCommitteeMember.objects.filter(committee='redressal')
    info = CommitteeInfo.objects.filter(committee='redressal').first()
    context = {
        'members': members,
        'info': info,
        'page_title': 'Grievance Redressal Committee',
        'breadcrumb': 'Grievance Redressal Committee',
    }
    return render(request, 'grievances/redressal.html', context)


def submit_grievance(request):
    if request.method == 'POST':
        form = GrievanceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your grievance has been submitted successfully. We will address it at the earliest.')
            return redirect('grievances:submit_grievance')
    else:
        form = GrievanceForm()
    context = {
        'form': form,
        'page_title': 'Submit Grievance',
        'breadcrumb': 'Submit a Grievance',
    }
    return render(request, 'grievances/submit_grievance.html', context)
