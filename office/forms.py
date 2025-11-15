from django import forms
from .models import Fee, Attendance, InternalMark, Student, Staff
from django.contrib.auth.models import User

class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = ['status', 'receipt']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'receipt': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

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
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Student
        fields = [
            'username', 'password', 'apaar_id', 'name', 'gender', 'caste',
            'category', 'address', 'guardian_name', 'student_phone_number',
            'parent_phone_number', 'department', 'semester', 'class_in_charge'
        ]
        widgets = {
            'apaar_id': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'caste': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'student_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'parent_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'class_in_charge': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = User.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        student = super().save(commit=False)
        student.user = user
        student.save()
        return student

class StaffRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), help_text="Enter a strong password.")
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Confirm Password")

    class Meta:
        model = Staff
        fields = ['staff_type'] # Only staff_type from the Staff model
        widgets = {
            'staff_type': forms.Select(attrs={'class': 'form-control'}),
        }

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

