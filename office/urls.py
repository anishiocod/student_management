from django.urls import path
from . import views

app_name = 'office'

urlpatterns = [
    path('', views.home, name='home'),
    path('student/detail/', views.student_detail, name='student_detail'),
    path('student/detail/<int:student_id>/', views.student_detail, name='student_detail_with_id'),
    path('staff/teaching/', views.teaching_staff_view, name='teaching_staff_view'),
    path('staff/non-teaching/', views.non_teaching_staff_view, name='non_teaching_staff_view'),
    path('notifications/', views.notification_list, name='notification_list'),
    path('staff/register-student/', views.register_student, name='register_student'),
    path('staff/register/', views.register_staff, name='register_staff'),
    path('student/<int:student_id>/update-fee/', views.update_fee_status, name='update_fee_status'),
    path('staff/manage-attendance/', views.manage_attendance, name='manage_attendance'),
    path('staff/upload-marks/', views.upload_internal_marks, name='upload_internal_marks'),
    path('admin/reports/', views.admin_reports_view, name='admin_reports'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('staff/dashboard/', views.office_staff_dashboard, name='office_staff_dashboard'),
]
