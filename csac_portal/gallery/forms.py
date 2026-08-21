from django import forms
from .models import GalleryItem


class GalleryItemForm(forms.ModelForm):
    class Meta:
        model = GalleryItem
        fields = [
            'category', 'gallery_type', 'title', 'description', 
            'image', 'image_url', 'video_url', 'news_source', 
            'date', 'order', 'is_active', 'is_homepage_highlight', 'highlight_subtitle'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput) and field_name not in ['image']:
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()
