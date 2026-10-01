from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms

from accounts.rich_text import clean_rich_text

from .models import AdmissionSubmitInstruction, EnrollmentInstruction


class AdmissionSubmitInstructionForm(forms.ModelForm):
    class Meta:
        model = AdmissionSubmitInstruction
        fields = ('heading', 'notice', 'sort_order', 'is_active')
        widgets = {
            'heading': forms.TextInput(attrs={
                'placeholder': 'e.g. Important — read before submitting',
                'size': 70,
            }),
            'notice': CKEditor5Widget(config_name='full'),
        }
        help_texts = {
            'heading': 'Displayed as the popup title when students submit their application.',
            'notice': 'Rich text with full formatting. Shown in the submit confirmation popup.',
            'sort_order': 'Lower numbers appear first if multiple active instructions exist.',
        }

    def clean_heading(self):
        heading = (self.cleaned_data.get('heading') or '').strip()
        if not heading:
            raise forms.ValidationError('Heading cannot be empty.')
        return heading

    def clean_notice(self):
        return clean_rich_text(self.cleaned_data.get('notice'), field_label='Notice content')


class EnrollmentInstructionForm(forms.ModelForm):
    class Meta:
        model = EnrollmentInstruction
        fields = ('college_title', 'title', 'content_html', 'is_active')
        widgets = {
            'college_title': forms.TextInput(attrs={
                'placeholder': 'चैतन्य साइंस एंड आर्ट्स कॉलेज, पामगढ़',
                'size': 70,
            }),
            'title': forms.TextInput(attrs={
                'placeholder': 'छात्र नामांकन (Enrollment) प्रक्रिया — चरण-दर-चरण निर्देश',
                'size': 70,
            }),
            'content_html': CKEditor5Widget(config_name='full'),
        }
        help_texts = {
            'college_title': 'Header title displayed at the top of the enrollment popup.',
            'title': 'Subheading describing the process or notice name.',
            'content_html': 'Step-by-step instructions displayed in the popup. Supports rich formatting.',
            'is_active': 'Check to display this instruction popup on student dashboards.',
        }

    def clean_title(self):
        title = (self.cleaned_data.get('title') or '').strip()
        if not title:
            raise forms.ValidationError('Title cannot be empty.')
        return title

    def clean_content_html(self):
        return clean_rich_text(self.cleaned_data.get('content_html'), field_label='Instruction content')