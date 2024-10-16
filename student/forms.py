# student/forms.py

from django import forms
from .models import Student

class StudentRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    class Meta:
        model = Student
        fields = ['username', 'email', 'first_name', 'last_name', 'school']  # Add first_name and last_name

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Ensure both password fields match
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data

    def save(self, commit=True):
        student = super(StudentRegistrationForm, self).save(commit=False)
        student.set_password(self.cleaned_data["password1"])  # Use password1 for setting the password
        if commit:
            student.save()
        return student
