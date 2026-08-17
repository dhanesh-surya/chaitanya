from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    path('department/<slug:slug>/', views.department_detail, name='department_detail'),
    path('programs/', views.programs, name='programs'),
    path('academic-calendar/', views.academic_calendar, name='academic_calendar'),
]
