from django import forms
from .models import Fee, Attendance, InternalMark, Student
from django.contrib.auth.models import User

class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = ['status', 'receipt']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'status']

class InternalMarkForm(forms.ModelForm):
    class Meta:
        model = InternalMark
        fields = ['student', 'subject', 'marks']

class StudentRegistrationForm(forms.ModelForm):
    # Fields for the User model
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = [
            'username', 'password', 'apaar_id', 'name', 'gender', 'caste',
            'category', 'address', 'guardian_name', 'student_phone_number',
            'parent_phone_number', 'department', 'semester', 'class_in_charge'
        ]

    def save(self, commit=True):
        user = User.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        student = super().save(commit=False)
        student.user = user
        student.save()
        return student
