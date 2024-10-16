from django import forms
from .models import School

class SchoolRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = School
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        school = super().save(commit=False)
        school.set_password(self.cleaned_data['password'])
        if commit:
            school.save()
        return school
