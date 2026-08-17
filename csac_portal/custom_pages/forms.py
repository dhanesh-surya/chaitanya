from django import forms
from .models import (CustomPage, CustomPageSlide, CustomPageMember, 
                     CustomPageActivity, CustomPageEventLink, CustomPageGalleryImage)

class CustomPageForm(forms.ModelForm):
    class Meta:
        model = CustomPage
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Enter rich text or HTML description here...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class CustomPageSlideForm(forms.ModelForm):
    class Meta:
        model = CustomPageSlide
        fields = '__all__'
        widgets = {
            'caption': forms.TextInput(attrs={'class': 'vTextField form-control', 'placeholder': 'Slide Caption'}),
            'order': forms.NumberInput(attrs={'class': 'vIntegerField form-control'}),
        }


class CustomPageMemberForm(forms.ModelForm):
    class Meta:
        model = CustomPageMember
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'vTextField form-control', 'placeholder': 'Full Name'}),
            'designation': forms.TextInput(attrs={'class': 'vTextField form-control', 'placeholder': 'e.g. Professor, Club Lead'}),
            'role': forms.TextInput(attrs={'class': 'vTextField form-control', 'placeholder': 'e.g. Coordinator, Member'}),
            'email': forms.EmailInput(attrs={'class': 'vTextField form-control', 'placeholder': 'e.g. member@chaitanyacg.ac.in'}),
            'phone': forms.TextInput(attrs={'class': 'vTextField form-control', 'placeholder': 'e.g. +91-XXXXXXXXXX'}),
            'order': forms.NumberInput(attrs={'class': 'vIntegerField form-control'}),
        }


class CustomPageActivityForm(forms.ModelForm):
    class Meta:
        model = CustomPageActivity
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'vTextField form-control', 'placeholder': 'Activity Title'}),
            'description': forms.Textarea(attrs={'class': 'vLargeTextField form-control', 'rows': 4, 'placeholder': 'Brief description'}),
            'date': forms.DateInput(attrs={'class': 'vDateField form-control', 'type': 'date'}),
            'order': forms.NumberInput(attrs={'class': 'vIntegerField form-control'}),
        }


class CustomPageEventLinkForm(forms.ModelForm):
    class Meta:
        model = CustomPageEventLink
        fields = '__all__'
        widgets = {
            'order': forms.NumberInput(attrs={'class': 'vIntegerField form-control'}),
        }


class CustomPageGalleryImageForm(forms.ModelForm):
    class Meta:
        model = CustomPageGalleryImage
        fields = '__all__'
        widgets = {
            'caption': forms.TextInput(attrs={'class': 'vTextField form-control', 'placeholder': 'Gallery Image Caption'}),
            'order': forms.NumberInput(attrs={'class': 'vIntegerField form-control'}),
        }
