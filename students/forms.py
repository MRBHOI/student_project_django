from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student
import re


class StudentForm(forms.ModelForm):
    date_of_admission = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Student
        fields = ['full_name', 'email', 'phone', 'course', 'date_of_admission']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit phone number'}),
            'course': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter course name'}),
        }

    def clean_full_name(self):
        name = self.cleaned_data.get('full_name')
        if any(char.isdigit() for char in name):
            raise forms.ValidationError("Name should not contain numbers.")
        return name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\d{10}$', phone):
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Student.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("A student with this email already exists.")
        return email


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
