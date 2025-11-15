from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=100)
    degree_type = models.CharField(max_length=50, 
                                   choices=[('FYUGP', 'FYUGP (4-year)'), 
                                            ('Regular', 'Regular (3-year)'),
                                            ('Masters', 'Masters (2-year)')])

    def __str__(self):
        return self.name

class Semester(models.Model):
    name = models.CharField(max_length=2, choices=[(f'S{i}', f'S{i}') for i in range(1, 9)])

    def __str__(self):
        return self.name

class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    subject_type = models.CharField(max_length=50, choices=[
        ('Major 1', 'Major 1'),
        ('Major 2', 'Major 2'),
        ('Minor 1', 'Minor 1'),
        ('Minor 2', 'Minor 2'),
        ('VAC 1', 'VAC 1'),
        ('VAC 2', 'VAC 2'),
        ('DSE', 'DSE'),
        ('SEC', 'SEC'),
        ('MDC', 'MDC'),
        ('AEC English', 'AEC English'),
        ('AEC Other', 'AEC Other'),
    ])

    def __str__(self):
        return f"{self.name} ({self.course.name} - {self.semester.name}) - {self.subject_type}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    apaar_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    caste = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    address = models.TextField()
    guardian_name = models.CharField(max_length=100)
    student_phone_number = models.CharField(max_length=15)
    parent_phone_number = models.CharField(max_length=15)
    department = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    class_in_charge = models.ForeignKey('Staff', on_delete=models.SET_NULL, null=True, blank=True, related_name='students_in_charge')

    def __str__(self):
        return self.name

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_type = models.CharField(max_length=20, choices=[('Teaching', 'Teaching'), ('Non-Teaching', 'Non-Teaching')])

    def __str__(self):
        return self.user.username

class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Not Paid', 'Not Paid')])
    receipt = models.FileField(upload_to='fee_receipts/', null=True, blank=True)

    def __str__(self):
        return f"{self.student.name} - {self.semester.name} Fee"

class Notification(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"

class InternalMark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.FloatField()

    def __str__(self):
        return f"{self.student.name} - {self.subject.name} - {self.marks}"