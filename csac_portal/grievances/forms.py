from django import forms
from .models import GrievanceSubmission


class GrievanceForm(forms.ModelForm):
    class Meta:
        model = GrievanceSubmission
        fields = ('grievance_type', 'complainant_name', 'email', 'mobile', 'roll_number', 'subject', 'description', 'supporting_document')
        widgets = {
            'grievance_type': forms.Select(attrs={'class': 'form-select'}),
            'complainant_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91-XXXXXXXXXX'}),
            'roll_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Roll Number (if applicable)'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief subject of your grievance'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe your grievance in detail...'}),
        }
        labels = {
            'grievance_type': 'Type of Grievance',
            'complainant_name': 'Your Name',
            'roll_number': 'Roll Number (Optional)',
        }
