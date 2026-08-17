from django.urls import path
from . import views

app_name = 'naac'

urlpatterns = [
    path('', views.naac_home, name='naac_home'),
    path('iqac/', views.iqac, name='iqac'),
    path('iiqa/', views.iiqa, name='iiqa'),
    path('ssr/', views.ssr, name='ssr'),
    path('dvv/', views.dvv, name='dvv'),
    path('atr/', views.atr, name='atr'),
]
