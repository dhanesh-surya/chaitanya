from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('admission/', views.admission, name='admission'),
    path('admission/online/', views.online_admission, name='online_admission'),
    path('fee-structure/', views.fee_structure, name='fee_structure'),
    path('scholarship/', views.scholarship, name='scholarship'),
    path('alumni/', views.alumni, name='alumni'),
    path('library/', views.library, name='library'),
    path('merit-list/', views.merit_list, name='merit_list'),
    path('syllabus/', views.syllabus, name='syllabus'),
]
