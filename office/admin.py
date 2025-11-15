from django.contrib import admin
from .models import Course, Semester, Subject, Student, Staff, Fee, Notification, Attendance, InternalMark

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'degree_type')
    list_filter = ('degree_type',)
    search_fields = ('name',)

class SemesterAdmin(admin.ModelAdmin):
    list_display = ('name',)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'semester', 'subject_type')
    list_filter = ('course', 'semester', 'subject_type')
    search_fields = ('name', 'course__name')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'apaar_id', 'department', 'semester', 'class_in_charge')
    list_filter = ('department', 'semester', 'gender', 'caste', 'category')
    search_fields = ('name', 'apaar_id', 'department__name')
    list_per_page = 20

class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'staff_type')
    list_filter = ('staff_type',)
    search_fields = ('user__username',)

class FeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'semester', 'status')
    list_filter = ('semester', 'status')
    search_fields = ('student__name', 'semester__name')
    list_per_page = 20

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'created_at')
    list_per_page = 20

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status')
    list_filter = ('date', 'status')
    search_fields = ('student__name',)
    list_per_page = 20

class InternalMarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'marks')
    list_filter = ('subject',)
    search_fields = ('student__name', 'subject__name')
    list_per_page = 20

admin.site.register(Course, CourseAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Fee, FeeAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(InternalMark, InternalMarkAdmin)
