from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('academics/', include('academics.urls', namespace='academics')),
    path('students/', include('students.urls', namespace='students')),
    path('naac/', include('naac.urls', namespace='naac')),
    path('grievances/', include('grievances.urls', namespace='grievances')),
    path('gallery/', include('gallery.urls', namespace='gallery')),
    path('feedback/', include('feedback.urls', namespace='feedback')),
    path('pages/', include('custom_pages.urls', namespace='custom_pages')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
