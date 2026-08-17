from django.urls import path
from . import views

app_name = 'custom_pages'

urlpatterns = [
    path('<slug:slug>/', views.custom_page_detail, name='custom_page_detail'),
]
