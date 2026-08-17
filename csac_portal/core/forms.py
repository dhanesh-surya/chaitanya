from django import forms
from .models import (
    SiteSettings, CareerGuidanceSubmission, AboutPage, Committee,
    CommitteeMember, CommitteeActivity, CommitteeGalleryImage,
    Policy, Notice, Event, UGCTable, UGCDocument,
    UGCPageSettings, UGCGrant, BreadcrumbSettings, PageBreadcrumb,
    NSSPageSettings, NSSActivity, NSSGalleryImage,
    IICPageSettings, IICGalleryImage, CampusMedia, Testimonial,
    Infrastructure, InfrastructureImage, AccreditationLogo, QuickLinkCard,
    Product, ProductInquiry, ProductCategory, ProductImage, ProductReview,
    SportsPageSettings, SportsGalleryImage, TeachingStaffPageSettings, NonTeachingStaffPageSettings,
    NonTeachingStaffMember,
    NEPTab, NEPTabFile, NEPTabLink,
    LibraryPageSettings, LibraryBookCategory, LibraryResource, LibraryBookSuggestion, LibraryGalleryImage,
    MenuItem
)

class CareerGuidanceForm(forms.ModelForm):
    class Meta:
        model = CareerGuidanceSubmission
        fields = ['fname', 'lname', 'email', 'phone', 'msg']
        widgets = {
            'fname': forms.TextInput(attrs={'id': 'fname', 'placeholder': 'First Name', 'required': True}),
            'lname': forms.TextInput(attrs={'id': 'lname', 'placeholder': 'Last Name', 'required': True}),
            'email': forms.EmailInput(attrs={'id': 'email', 'placeholder': 'Email..', 'required': True}),
            'phone': forms.TextInput(attrs={'id': 'Phone', 'placeholder': 'Phone', 'required': True, 'type': 'number'}),
            'msg': forms.Textarea(attrs={'id': 'msg', 'placeholder': 'Enter Your Comments'}),
        }


class AboutPageForm(forms.ModelForm):
    class Meta:
        model = AboutPage
        fields = '__all__'
        widgets = {
            'about_us_description_1': forms.Textarea(attrs={'rows': 4}),
            'about_us_description_2': forms.Textarea(attrs={'rows': 4}),
            'about_us_description_3': forms.Textarea(attrs={'rows': 4}),
            'mission_statement': forms.Textarea(attrs={'rows': 3}),
            'vision_text': forms.Textarea(attrs={'rows': 4}),
            'mission_text_1': forms.Textarea(attrs={'rows': 3}),
            'mission_text_2': forms.Textarea(attrs={'rows': 3}),
            'governance_text': forms.Textarea(attrs={'rows': 6}),
            'features_list': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Enter distinctive features, one per line...'}),
            'testimonial_text': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class CommitteeForm(forms.ModelForm):
    class Meta:
        model = Committee
        fields = ['name', 'slug', 'description', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class CommitteeMemberForm(forms.ModelForm):
    class Meta:
        model = CommitteeMember
        fields = ['committee', 'name', 'designation', 'role_in_committee', 'order']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class CommitteeActivityForm(forms.ModelForm):
    class Meta:
        model = CommitteeActivity
        fields = ['committee', 'title', 'description', 'date', 'image', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput) and field_name != 'image':
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class CommitteeGalleryImageForm(forms.ModelForm):
    class Meta:
        model = CommitteeGalleryImage
        fields = ['committee', 'image', 'caption', 'order']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput) and field_name != 'image':
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class PolicyForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = ['title', 'document', 'document_url', 'description', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput) and field_name != 'document':
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'category', 'document', 'document_url', 'published_date', 'show_in_marquee', 'marquee_flag', 'is_active']
        widgets = {
            'published_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput) and field_name != 'document':
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'date', 'time', 'location', 'description', 
            'image', 'image_url', 'brochure', 'registration_link', 
            'youtube_url', 'link', 'is_active'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput) and field_name not in ['image', 'brochure']:
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class UGCTableForm(forms.ModelForm):
    class Meta:
        model = UGCTable
        fields = ['name', 'order', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class UGCDocumentForm(forms.ModelForm):
    class Meta:
        model = UGCDocument
        fields = ['ugc_table', 'sn', 'title', 'file', 'file_url']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput) and field_name != 'file':
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class UGCPageSettingsForm(forms.ModelForm):
    class Meta:
        model = UGCPageSettings
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'status_2f_12b_text': forms.Textarea(attrs={'rows': 4}),
            'benefits_list': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Enter benefits, one per line...'}),
            'autonomy_status_text': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class UGCGrantForm(forms.ModelForm):
    class Meta:
        model = UGCGrant
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = '__all__'
        color_picker_style = 'width: 80px; height: 40px; border: 1px solid #ccc; border-radius: 4px; padding: 2px; cursor: pointer;'
        widgets = {
            'google_maps_embed': forms.Textarea(attrs={'rows': 4}),
            
            # Color pickers
            'college_name_en_font_color': forms.TextInput(attrs={'type': 'color', 'style': color_picker_style}),
            'college_name_hi_font_color': forms.TextInput(attrs={'type': 'color', 'style': color_picker_style}),
            'tagline_font_color': forms.TextInput(attrs={'type': 'color', 'style': color_picker_style}),
            'address_line1_font_color': forms.TextInput(attrs={'type': 'color', 'style': color_picker_style}),
            'address_line2_font_color': forms.TextInput(attrs={'type': 'color', 'style': color_picker_style}),
            
            # Font family selections with datalists
            'college_name_en_font_family': forms.TextInput(attrs={'list': 'font-families-datalist'}),
            'college_name_hi_font_family': forms.TextInput(attrs={'list': 'font-families-datalist'}),
            'tagline_font_family': forms.TextInput(attrs={'list': 'font-families-datalist'}),
            'address_line1_font_family': forms.TextInput(attrs={'list': 'font-families-datalist'}),
            'address_line2_font_family': forms.TextInput(attrs={'list': 'font-families-datalist'}),
            
            # Font size selections with datalists
            'college_name_en_font_size': forms.TextInput(attrs={'list': 'font-sizes-datalist'}),
            'college_name_hi_font_size': forms.TextInput(attrs={'list': 'font-sizes-datalist'}),
            'tagline_font_size': forms.TextInput(attrs={'list': 'font-sizes-datalist'}),
            'address_line1_font_size': forms.TextInput(attrs={'list': 'font-sizes-datalist'}),
            'address_line2_font_size': forms.TextInput(attrs={'list': 'font-sizes-datalist'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        excluded_fields = [
            'college_logo', 'college_logo_mobile', 'logo2', 'logo3', 'logo4', 'logo5',
            'college_name_en_font_color', 'college_name_hi_font_color', 'tagline_font_color',
            'address_line1_font_color', 'address_line2_font_color', 'header_image'
        ]
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput) and field_name not in excluded_fields:
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class BreadcrumbSettingsForm(forms.ModelForm):
    class Meta:
        model = BreadcrumbSettings
        fields = ['default_image', 'default_image_url', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput,)) and field_name != 'default_image':
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class PageBreadcrumbForm(forms.ModelForm):
    class Meta:
        model = PageBreadcrumb
        fields = ['page_key', 'custom_image', 'custom_image_url', 'use_default', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput,)) and field_name != 'custom_image':
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class NSSPageSettingsForm(forms.ModelForm):
    class Meta:
        model = NSSPageSettings
        fields = '__all__'
        widgets = {
            'banner_description': forms.Textarea(attrs={'rows': 4}),
            'about_description': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput,)) and field_name not in ['banner_image', 'banner_icon']:
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class NSSActivityForm(forms.ModelForm):
    class Meta:
        model = NSSActivity
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput,)):
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class NSSGalleryImageForm(forms.ModelForm):
    class Meta:
        model = NSSGalleryImage
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput,)) and field_name != 'image':
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class IICPageSettingsForm(forms.ModelForm):
    class Meta:
        model = IICPageSettings
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput,)) and field_name not in ['about_image_1', 'about_image_2']:
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class IICGalleryImageForm(forms.ModelForm):
    class Meta:
        model = IICGalleryImage
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput,)) and field_name != 'image':
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class CampusMediaForm(forms.ModelForm):
    class Meta:
        model = CampusMedia
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput,)) and field_name != 'image':
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()



class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = '__all__'
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput,)) and field_name != 'photo':
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class InfrastructureForm(forms.ModelForm):
    class Meta:
        model = Infrastructure
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput,)):
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class InfrastructureImageForm(forms.ModelForm):
    class Meta:
        model = InfrastructureImage
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput,)) and field_name != 'image':
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class AccreditationLogoForm(forms.ModelForm):
    class Meta:
        model = AccreditationLogo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput,)) and field_name != 'image':
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class QuickLinkCardForm(forms.ModelForm):
    class Meta:
        model = QuickLinkCard
        fields = '__all__'
        widgets = {
            'bg_color': forms.TextInput(attrs={'type': 'color', 'style': 'width: 80px; height: 40px; border: 1px solid #ccc; border-radius: 4px; padding: 2px; cursor: pointer;'}),
            'overlay_color': forms.TextInput(attrs={'type': 'color', 'style': 'width: 80px; height: 40px; border: 1px solid #ccc; border-radius: 4px; padding: 2px; cursor: pointer;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['bg_color', 'overlay_color', 'bg_image', 'icon'] and not isinstance(field.widget, (forms.CheckboxInput,)):
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput,)) and field_name != 'image':
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class ProductInquiryForm(forms.ModelForm):
    class Meta:
        model = ProductInquiry
        fields = ['product', 'name', 'email', 'phone', 'message']
        widgets = {
            'product': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'placeholder': 'Your Full Name', 'required': True}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email Address', 'required': True}),
            'phone': forms.TextInput(attrs={'placeholder': 'Your Phone Number', 'required': True, 'type': 'tel'}),
            'message': forms.Textarea(attrs={'placeholder': 'Write any comments or specific requests here...', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'product':
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['reviewer_name', 'reviewer_email', 'rating', 'review_text']
        widgets = {
            'reviewer_name': forms.TextInput(attrs={'placeholder': 'Your Full Name', 'required': True}),
            'reviewer_email': forms.EmailInput(attrs={'placeholder': 'Your Email Address', 'required': True}),
            'rating': forms.Select(choices=[(i, f"{i} Stars") for i in range(5, 0, -1)]),
            'review_text': forms.Textarea(attrs={'placeholder': 'Share your experience with this product...', 'rows': 4, 'required': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class TeachingStaffPageSettingsForm(forms.ModelForm):
    class Meta:
        model = TeachingStaffPageSettings
        fields = ['title', 'subtitle']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Faculty List 2025-26'}),
            'subtitle': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class NonTeachingStaffPageSettingsForm(forms.ModelForm):
    class Meta:
        model = NonTeachingStaffPageSettings
        fields = ['title', 'subtitle']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Non-Teaching Staff'}),
            'subtitle': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class NonTeachingStaffMemberForm(forms.ModelForm):
    class Meta:
        model = NonTeachingStaffMember
        fields = [
            'name', 'designation', 'department_section',
            'qualification', 'contact', 'order', 'is_active',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter full name'}),
            'designation': forms.TextInput(attrs={'placeholder': 'e.g. Office Superintendent, Clerk'}),
            'department_section': forms.TextInput(attrs={'placeholder': 'e.g. Administration, Accounts'}),
            'qualification': forms.TextInput(attrs={'placeholder': 'e.g. B.Com., M.A.'}),
            'contact': forms.TextInput(attrs={'placeholder': 'Phone or email'}),
            'order': forms.NumberInput(attrs={'placeholder': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class SportsPageSettingsForm(forms.ModelForm):
    class Meta:
        model = SportsPageSettings
        fields = '__all__'
        widgets = {
            'page_intro': forms.Textarea(attrs={'rows': 4}),
            'facilities': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Enter one facility per line...'}),
            'achievements': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter one achievement per line...'}),
            'policies': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter one policy per line...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class SportsGalleryImageForm(forms.ModelForm):
    class Meta:
        model = SportsGalleryImage
        fields = '__all__'
        widgets = {
            'caption': forms.TextInput(attrs={'placeholder': 'Image caption (optional)'}),
            'sport_tag': forms.TextInput(attrs={'placeholder': 'e.g. Cricket, Volleyball, Athletics'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class NEPTabForm(forms.ModelForm):
    class Meta:
        model = NEPTab
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter tab title (e.g. ABC Portal)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class NEPTabFileForm(forms.ModelForm):
    class Meta:
        model = NEPTabFile
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'File label (e.g. Curriculum PDF)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class NEPTabLinkForm(forms.ModelForm):
    class Meta:
        model = NEPTabLink
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Link label (e.g. Digilocker web)'}),
            'url': forms.URLInput(attrs={'placeholder': 'https://example.com'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class LibraryPageSettingsForm(forms.ModelForm):
    class Meta:
        model = LibraryPageSettings
        fields = '__all__'
        widgets = {
            'page_intro': forms.Textarea(attrs={'rows': 4}),
            'about_library_text': forms.Textarea(attrs={'rows': 5}),
            'future_plan_text': forms.Textarea(attrs={'rows': 5}),
            'sections_text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Reference Section\nCirculation Section\nPeriodical Section'}),
            'about_services_text': forms.Textarea(attrs={'rows': 3}),
            'new_suggestion_text': forms.Textarea(attrs={'rows': 3}),
            'library_image_url': forms.TextInput(attrs={'placeholder': '/static/assets/images/feature/0001.png'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class LibraryBookCategoryForm(forms.ModelForm):
    class Meta:
        model = LibraryBookCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class LibraryResourceForm(forms.ModelForm):
    class Meta:
        model = LibraryResource
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class LibraryBookSuggestionForm(forms.ModelForm):
    class Meta:
        model = LibraryBookSuggestion
        fields = ['book_title', 'author', 'recommended_by', 'email', 'reason']
        widgets = {
            'book_title': forms.TextInput(attrs={'placeholder': 'Enter book title', 'required': True}),
            'author': forms.TextInput(attrs={'placeholder': 'Enter author name', 'required': True}),
            'recommended_by': forms.TextInput(attrs={'placeholder': 'Your name (student/faculty)', 'required': True}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your email address', 'required': True}),
            'reason': forms.Textarea(attrs={'placeholder': 'Why are you suggesting this book? (optional)', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class LibraryGalleryImageForm(forms.ModelForm):
    class Meta:
        model = LibraryGalleryImage
        fields = '__all__'
        widgets = {
            'caption': forms.TextInput(attrs={'placeholder': 'Image caption (optional)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['title', 'url', 'is_named_url', 'parent', 'order', 'is_active', 'open_in_new_tab']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add bootstrap class to form elements
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()
            else:
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-check-input".strip()

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get('url')
        is_named_url = cleaned_data.get('is_named_url')
        parent = cleaned_data.get('parent')
        
        # Prevent selecting itself as parent
        if self.instance.pk and parent == self.instance:
            raise forms.ValidationError("A menu item cannot be its own parent.")
            
        # Prevent cyclic dependency
        if parent:
            curr = parent
            while curr is not None:
                if self.instance.pk and curr.pk == self.instance.pk:
                    raise forms.ValidationError("A menu item cannot have its own descendant as a parent.")
                curr = curr.parent

        # Validate Named URL if checked
        if is_named_url and url:
            from django.urls import reverse, NoReverseMatch
            parts = url.split()
            url_name = parts[0]
            url_args = [arg.strip("'\"") for arg in parts[1:]]
            
            try:
                reverse(url_name, args=url_args)
            except NoReverseMatch:
                raise forms.ValidationError(
                    f"'{url}' is not a valid Django URL pattern or cannot be resolved with the provided arguments."
                )
        return cleaned_data


from .models import Leadership

class LeadershipForm(forms.ModelForm):
    class Meta:
        model = Leadership
        fields = ['name', 'qualification', 'email', 'photo', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 6}),
            'email': forms.EmailInput(attrs={'placeholder': 'e.g. principal@chaitanyacg.ac.in'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput) and field_name != 'photo':
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()


from .models import UploadedDocument

class UploadedDocumentForm(forms.ModelForm):
    class Meta:
        model = UploadedDocument
        fields = ['title', 'file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'file':
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()
            else:
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control-file".strip()


