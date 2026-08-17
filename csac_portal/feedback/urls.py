from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('student/', views.student_feedback, name='student_feedback'),
    path('parent/', views.parent_feedback, name='parent_feedback'),
    path('faculty/', views.faculty_feedback, name='faculty_feedback'),
    path('alumni/', views.alumni_feedback, name='alumni_feedback'),
    path('events/', views.event_feedback_list, name='event_feedback_list'),
    path('events/<slug:slug>/', views.event_feedback, name='event_feedback'),
    path(
        'events/<slug:slug>/thank-you/<int:response_id>/',
        views.event_feedback_success,
        name='event_feedback_success',
    ),
    path(
        'events/<slug:slug>/certificate/<int:response_id>/',
        views.event_feedback_certificate,
        name='event_feedback_certificate',
    ),
    # Legacy / short link for Admission Fest 2026
    path(
        'admission-fest-2026/',
        views.admission_fest_2026_feedback,
        name='admission_fest_2026_feedback',
    ),
]
