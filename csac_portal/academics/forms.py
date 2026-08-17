from django import forms
from .models import Department, DepartmentFaculty, DepartmentBanner, Program, ProgramType

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
        widgets = {
            'hod_message': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rich_text_fields = {'description'}
        file_fields = {'hod_photo', 'banner_image'}
        for field_name, field in self.fields.items():
            if (
                not isinstance(field.widget, forms.CheckboxInput)
                and field_name not in file_fields
                and field_name not in rich_text_fields
            ):
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class DepartmentFacultyForm(forms.ModelForm):
    class Meta:
        model = DepartmentFaculty
        fields = ['department', 'name', 'designation', 'qualification', 'specialization', 'photo', 'email', 'phone', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'vTextField form-control', 'placeholder': 'Enter full name'}),
            'designation': forms.TextInput(attrs={'class': 'vTextField form-control', 'placeholder': 'e.g. Assistant Professor, Professor'}),
            'qualification': forms.TextInput(attrs={'class': 'vTextField form-control', 'placeholder': 'e.g. M.Sc., Ph.D.'}),
            'specialization': forms.TextInput(attrs={'class': 'vTextField form-control', 'placeholder': 'e.g. Entomology, Organic Chemistry'}),
            'email': forms.EmailInput(attrs={'class': 'vTextField form-control', 'placeholder': 'e.g. faculty@chaitanyacg.ac.in'}),
            'phone': forms.TextInput(attrs={'class': 'vTextField form-control', 'placeholder': 'e.g. +91-XXXXXXXXXX'}),
        }


class DepartmentBannerForm(forms.ModelForm):
    class Meta:
        model = DepartmentBanner
        fields = ['department', 'image', 'caption', 'order']
        widgets = {
            'caption': forms.TextInput(attrs={'class': 'vTextField form-control', 'placeholder': 'e.g. Zoology Lab Banner'}),
            'order': forms.NumberInput(attrs={'class': 'vIntegerField form-control', 'placeholder': '0'}),
        }


class ProgramForm(forms.ModelForm):
    program_type = forms.ChoiceField(label='Program Type')

    class Meta:
        model = Program
        fields = '__all__'
        widgets = {
            'duration': forms.TextInput(attrs={'placeholder': 'e.g. 3 Years, 6 Semesters'}),
            'eligibility': forms.Textarea(attrs={'rows': 3}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        active_types = ProgramType.objects.filter(is_active=True).order_by('order', 'name')
        self.fields['program_type'].choices = [(pt.code, pt.name) for pt in active_types]

        if self.instance.pk and self.instance.program_type:
            stored_type = self.instance.program_type
            if not active_types.filter(code=stored_type).exists():
                legacy_type = (
                    ProgramType.objects.filter(name=stored_type).first()
                    or ProgramType.objects.filter(code__iexact=stored_type).first()
                )
                if legacy_type:
                    self.initial['program_type'] = legacy_type.code

        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class ProgramTypeForm(forms.ModelForm):
    class Meta:
        model = ProgramType
        fields = '__all__'
        widgets = {
            'icon_class': forms.TextInput(attrs={'placeholder': 'e.g. fas fa-graduation-cap'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()



