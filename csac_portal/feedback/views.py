from django.core import signing
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .forms import (
    StudentFeedbackForm,
    ParentFeedbackForm,
    FacultyFeedbackForm,
    AlumniFeedbackForm,
    EventFeedbackResponseForm,
)
from .models import EventFeedbackCampaign, EventFeedbackResponse
from .event_i18n import get_ui, localized_campaign_copy, resolve_lang_from_request
from .certificate import certificate_http_response, certificate_number

CERT_SIGNING_SALT = 'feedback.participation-certificate'


def student_feedback(request):
    if request.method == 'POST':
        form = StudentFeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your valuable feedback!')
            return redirect('feedback:student_feedback')
    else:
        form = StudentFeedbackForm()
    return render(request, 'feedback/student_feedback.html', {
        'form': form, 'page_title': "Student's Feedback", 'breadcrumb': "Student's Feedback Form"
    })


def parent_feedback(request):
    if request.method == 'POST':
        form = ParentFeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your valuable feedback!')
            return redirect('feedback:parent_feedback')
    else:
        form = ParentFeedbackForm()
    return render(request, 'feedback/parent_feedback.html', {
        'form': form, 'page_title': "Parent's Feedback", 'breadcrumb': "Parent's Feedback Form"
    })


def faculty_feedback(request):
    if request.method == 'POST':
        form = FacultyFeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your valuable feedback!')
            return redirect('feedback:faculty_feedback')
    else:
        form = FacultyFeedbackForm()
    return render(request, 'feedback/faculty_feedback.html', {
        'form': form, 'page_title': "Faculty's Feedback", 'breadcrumb': "Faculty's Feedback Form"
    })


def alumni_feedback(request):
    if request.method == 'POST':
        form = AlumniFeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your valuable feedback!')
            return redirect('feedback:alumni_feedback')
    else:
        form = AlumniFeedbackForm()
    return render(request, 'feedback/alumni_feedback.html', {
        'form': form, 'page_title': "Alumni's Feedback", 'breadcrumb': "Alumni's Feedback Form"
    })


def event_feedback_list(request):
    campaigns = EventFeedbackCampaign.objects.filter(is_active=True)
    return render(request, 'feedback/event_feedback_list.html', {
        'campaigns': campaigns,
        'page_title': 'Event Feedback',
        'breadcrumb': 'Event Feedback Forms',
    })


def event_feedback(request, slug):
    campaign = get_object_or_404(EventFeedbackCampaign, slug=slug)
    lang = resolve_lang_from_request(request)
    ui = get_ui(lang)
    copy = localized_campaign_copy(campaign, lang)

    if not campaign.is_active:
        messages.warning(request, ui['form_closed'])
        return redirect('feedback:event_feedback_list')

    if request.method == 'POST':
        form = EventFeedbackResponseForm(request.POST, campaign=campaign, lang=lang)
        if form.is_valid():
            response_obj = form.save()
            token = signing.dumps(
                {'id': response_obj.pk, 'slug': campaign.slug},
                salt=CERT_SIGNING_SALT,
            )
            return redirect(
                reverse(
                    'feedback:event_feedback_success',
                    kwargs={'slug': campaign.slug, 'response_id': response_obj.pk},
                )
                + f'?lang={lang}&token={token}'
            )
    else:
        form = EventFeedbackResponseForm(campaign=campaign, lang=lang)

    return render(request, 'feedback/event_feedback.html', {
        'form': form,
        'campaign': campaign,
        'copy': copy,
        't': ui,
        'lang': lang,
        'page_title': copy['title'],
        'breadcrumb': copy['title'],
    })


def _verify_certificate_token(token, response_id, slug):
    try:
        data = signing.loads(token, salt=CERT_SIGNING_SALT, max_age=60 * 60 * 24 * 30)
    except signing.BadSignature:
        return False
    return int(data.get('id', -1)) == int(response_id) and data.get('slug') == slug


def event_feedback_success(request, slug, response_id):
    """Thank-you page after feedback with certificate download link."""
    campaign = get_object_or_404(EventFeedbackCampaign, slug=slug)
    response_obj = get_object_or_404(EventFeedbackResponse, pk=response_id, campaign=campaign)
    lang = resolve_lang_from_request(request)
    ui = get_ui(lang)
    copy = localized_campaign_copy(campaign, lang)
    token = request.GET.get('token') or request.POST.get('token') or ''

    if not token or not _verify_certificate_token(token, response_id, slug):
        messages.warning(
            request,
            'This certificate link is invalid or has expired. Please submit the feedback form again.',
        )
        return redirect('feedback:event_feedback', slug=slug)

    cert_url = (
        reverse(
            'feedback:event_feedback_certificate',
            kwargs={'slug': slug, 'response_id': response_id},
        )
        + f'?lang={lang}&token={token}'
    )

    return render(request, 'feedback/event_feedback_success.html', {
        'campaign': campaign,
        'response_obj': response_obj,
        'copy': copy,
        't': ui,
        'lang': lang,
        'token': token,
        'certificate_url': cert_url,
        'certificate_number': certificate_number(response_obj),
        'page_title': copy['title'],
        'breadcrumb': copy['title'],
        'confirmation_message': copy['confirmation_message'],
    })


def event_feedback_certificate(request, slug, response_id):
    """Download / view participation certificate PDF."""
    campaign = get_object_or_404(EventFeedbackCampaign, slug=slug)
    response_obj = get_object_or_404(EventFeedbackResponse, pk=response_id, campaign=campaign)
    lang = resolve_lang_from_request(request)
    token = request.GET.get('token') or ''

    if not token or not _verify_certificate_token(token, response_id, slug):
        raise Http404('Invalid or expired certificate link.')

    return certificate_http_response(response_obj, lang=lang)


def admission_fest_2026_feedback(request):
    """Backward-compatible URL → Admission Fest 2026 campaign."""
    campaign = EventFeedbackCampaign.objects.filter(slug='admission-fest-2026').first()
    if campaign:
        return redirect('feedback:event_feedback', slug=campaign.slug)
    return redirect('feedback:event_feedback_list')
