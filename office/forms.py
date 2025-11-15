from django import forms
from .models import Fee, Attendance, InternalMark, Student, Staff
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

class StaffRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.")
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, help_text="Enter a strong password.")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = Staff
        fields = ['staff_type'] # Only staff_type from the Staff model

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        staff = super().save(commit=False)
        staff.user = user
        if commit:
            staff.save()
        return staff

