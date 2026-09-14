from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    # Public Catalogue & Home
    path('', views.library_home, name='home'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),

    # Student Portal & Circulation
    path('logout/', views.logout_view, name='logout'),
    path('student/login/', views.student_login_view, name='student_login'),
    path('student/register/', views.student_register_view, name='student_register'),
    path('student/logout/', views.student_logout_view, name='student_logout'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/requests/', views.my_requests, name='my_requests'),
    path('student/issued/', views.my_issued_books, name='my_issued'),
    path('student/history/', views.my_history, name='my_history'),
    path('student/action/request-book/', views.request_book_action, name='request_book'),
    path('student/action/cancel-request/<int:request_id>/', views.cancel_request_action, name='cancel_request'),
    path('student/action/return-request/<int:transaction_id>/', views.return_request_action, name='return_request'),

    # Staff / Librarian Operations Desk
    path('staff/login/', views.staff_login_view, name='staff_login'),
    path('librarian/dashboard/', views.librarian_dashboard, name='librarian_dashboard'),
    path('librarian/registrations/', views.student_registrations_queue, name='librarian_registrations'),
    path('librarian/registrations/<int:student_id>/approve/', views.approve_student_registration, name='approve_registration'),
    path('librarian/registrations/<int:student_id>/reject/', views.reject_student_registration, name='reject_registration'),
    path('librarian/requests/', views.requests_queue, name='librarian_requests'),
    path('librarian/requests/<int:request_id>/approve/', views.approve_request_action, name='approve_request'),
    path('librarian/requests/<int:request_id>/reject/', views.reject_request_action, name='reject_request'),
    path('librarian/issue/', views.issue_desk, name='librarian_issue'),
    path('librarian/issue/confirm/', views.confirm_issue_action, name='confirm_issue'),
    path('librarian/returns/', views.return_desk, name='librarian_returns'),
    path('librarian/returns/<int:transaction_id>/confirm/', views.confirm_return_action, name='confirm_return'),
    path('librarian/overdue/', views.overdue_monitor, name='librarian_overdue'),
    path('librarian/fines/<int:fine_id>/settle/', views.settle_fine_action, name='settle_fine'),

    # Library Administration
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/students/', views.admin_students_view, name='admin_students'),
    path('admin/students/add/', views.admin_add_student_view, name='admin_add_student'),
    path('admin/students/<int:student_id>/reset-password/', views.admin_reset_student_password, name='admin_reset_password'),
    path('admin/import/', views.import_excel_view, name='admin_import'),
    path('admin/import/commit/', views.import_commit_action, name='admin_import_commit'),
    path('admin/rules/', views.rules_settings_view, name='admin_rules'),
    path('admin/audit/', views.audit_logs_view, name='admin_audit'),
    path('admin/reports/', views.circulation_reports_view, name='admin_reports'),
]
