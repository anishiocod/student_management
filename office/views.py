from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Student, Staff, Notification, Fee, Attendance, InternalMark, Subject
from .forms import FeeForm, AttendanceForm, InternalMarkForm, StudentRegistrationForm
from django.utils import timezone

def is_teaching_staff(user):
    return user.is_authenticated and hasattr(user, 'staff') and user.staff.staff_type == 'Teaching'

def is_non_teaching_staff(user):
    return user.is_authenticated and hasattr(user, 'staff') and user.staff.staff_type == 'Non-Teaching'

def home(request):
    return render(request, 'office/home.html')

@login_required
def student_detail(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        # Handle case where the logged-in user is not a student
        return render(request, 'office/not_a_student.html')
    return render(request, 'office/student_detail.html', {'student': student})

@user_passes_test(is_teaching_staff)
def teaching_staff_view(request):
    students = Student.objects.filter(class_in_charge=request.user.staff)
    return render(request, 'office/teaching_staff_view.html', {'students': students})

@user_passes_test(is_non_teaching_staff)
def non_teaching_staff_view(request):
    students = Student.objects.all()
    return render(request, 'office/non_teaching_staff_view.html', {'students': students})

@user_passes_test(is_non_teaching_staff)
def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('non_teaching_staff_view')
    else:
        form = StudentRegistrationForm()
    return render(request, 'office/register_student.html', {'form': form})


@user_passes_test(is_non_teaching_staff)
def update_fee_status(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    fee, created = Fee.objects.get_or_create(student=student, semester=student.semester)

    if request.method == 'POST':
        form = FeeForm(request.POST, request.FILES, instance=fee)
        if form.is_valid():
            form.save()
            return redirect('non_teaching_staff_view')
    else:
        form = FeeForm(instance=fee)

    return render(request, 'office/update_fee_status.html', {'form': form, 'student': student})

@user_passes_test(is_teaching_staff)
def manage_attendance(request):
    teacher = request.user.staff
    students = Student.objects.filter(class_in_charge=teacher)
    date = request.GET.get('date', timezone.now().date())

    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'student_{student.id}')
            if status:
                Attendance.objects.update_or_create(
                    student=student,
                    date=date,
                    defaults={'status': status}
                )
        return redirect('manage_attendance')

    attendance_records = Attendance.objects.filter(date=date, student__in=students)
    attendance_map = {record.student_id: record.status for record in attendance_records}

    return render(request, 'office/manage_attendance.html', {
        'students': students,
        'date': date,
        'attendance_map': attendance_map,
    })

@user_passes_test(is_teaching_staff)
def upload_internal_marks(request):
    teacher = request.user.staff
    # Get all students under the teacher's charge
    students_in_charge = Student.objects.filter(class_in_charge=teacher)
    
    # Get all subjects related to the courses/semesters of those students
    student_departments = students_in_charge.values_list('department', flat=True)
    student_semesters = students_in_charge.values_list('semester', flat=True)
    relevant_subjects = Subject.objects.filter(
        course__in=student_departments,
        semester__in=student_semesters
    ).distinct()

    if request.method == 'POST':
        form = InternalMarkForm(request.POST)
        if form.is_valid():
            # Additional security check: ensure the selected student is one the teacher is in charge of
            if form.cleaned_data['student'] in students_in_charge:
                form.save()
            return redirect('upload_internal_marks')
    else:
        form = InternalMarkForm()
        form.fields['student'].queryset = students_in_charge
        form.fields['subject'].queryset = relevant_subjects

    return render(request, 'office/upload_internal_marks.html', {'form': form})

@login_required
def notification_list(request):
    notifications = Notification.objects.all().order_by('-created_at')
    return render(request, 'office/notification_list.html', {'notifications': notifications})

@user_passes_test(is_non_teaching_staff)
def admin_reports_view(request):
    return render(request, 'office/admin_reports.html')