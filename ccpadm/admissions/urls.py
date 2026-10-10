from django.urls import path

from . import enrollment_views, nep_ug_views, views

urlpatterns = [
    path('fill-form/', views.fill_admission_form, name='fill_admission_form'),
    path('preview/', views.preview_application, name='preview_application'),
    path('my-application/', views.my_application, name='my_application'),
    path('print/<str:app_no>/', views.print_application, name='print_application'),
    path('download-pdf/', views.download_pdf_page, name='download_pdf_page'),
    path('pdf/<str:app_no>/', views.download_pdf, name='download_pdf'),
    path('enrollment/', enrollment_views.enrollment_form, name='enrollment_form'),
    path('enrollment/print/', enrollment_views.enrollment_print, name='enrollment_print_default'),
    path('enrollment/print/<str:enrollment_no>/', enrollment_views.enrollment_print, name='enrollment_print'),
    path('enrollment/receipt/', enrollment_views.enrollment_fee_receipt, name='enrollment_receipt_default'),
    path('enrollment/receipt/<str:enrollment_no>/', enrollment_views.enrollment_fee_receipt, name='enrollment_receipt'),
    path('enrollment/cancel/', enrollment_views.cancel_enrollment, name='cancel_enrollment'),
    path('nep-ug/', nep_ug_views.nep_ug_enrollment_form, name='nep_ug_enrollment_form'),
    path('nep-ug/print/', nep_ug_views.nep_ug_print, name='nep_ug_print_default'),
    path('nep-ug/print/<str:enrollment_no>/', nep_ug_views.nep_ug_print, name='nep_ug_print'),
    path('nep-ug/receipt/', nep_ug_views.nep_ug_fee_receipt, name='nep_ug_receipt_default'),
    path('nep-ug/receipt/<str:enrollment_no>/', nep_ug_views.nep_ug_fee_receipt, name='nep_ug_receipt'),
    path('nep-ug/cancel/', nep_ug_views.cancel_nep_ug_enrollment, name='cancel_nep_ug_enrollment'),
    path('api/courses/', views.courses_api, name='courses_api'),
    path('api/save-draft/', views.save_draft_api, name='save_draft_api'),
    path('api/load-draft/', views.load_draft_api, name='load_draft_api'),
    path('api/submit/', views.submit_application, name='submit_application'),
]