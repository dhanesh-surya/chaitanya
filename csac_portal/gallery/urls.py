from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('images/', views.image_gallery, name='image_gallery'),
    path('videos/', views.video_gallery, name='video_gallery'),
    path('news/', views.news_gallery, name='news_gallery'),
]
