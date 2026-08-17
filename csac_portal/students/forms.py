from django import forms
from django.utils.safestring import mark_safe
from .models import OnlineAdmission

RATING_CHOICES = [(i, '⭐' * i) for i in range(1, 6)]


class OnlineAdmissionForm(forms.ModelForm):
    class Meta:
        model = OnlineAdmission
        exclude = ('status',)
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91-XXXXXXXXXX'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'program_applied': forms.TextInput(attrs={'class': 'form-control'}),
            'last_exam_passed': forms.TextInput(attrs={'class': 'form-control'}),
            'last_exam_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
