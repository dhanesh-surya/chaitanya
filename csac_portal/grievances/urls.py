from django.urls import path
from . import views

app_name = 'grievances'

urlpatterns = [
    path('anti-ragging/', views.anti_ragging, name='anti_ragging'),
    path('icc/', views.icc, name='icc'),
    path('redressal/', views.redressal, name='redressal'),
    path('submit/', views.submit_grievance, name='submit_grievance'),
]
