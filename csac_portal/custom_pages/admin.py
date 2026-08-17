from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import (CustomPage, CustomPageSlide, CustomPageMember, 
                     CustomPageActivity, CustomPageEventLink, CustomPageGalleryImage)
from .forms import (CustomPageForm, CustomPageSlideForm, CustomPageMemberForm, 
                    CustomPageActivityForm, CustomPageEventLinkForm, CustomPageGalleryImageForm)


class CustomPageSlideInline(admin.TabularInline):
    model = CustomPageSlide
    form = CustomPageSlideForm
    extra = 1
    fields = ('image', 'caption', 'order')


class CustomPageMemberInline(admin.TabularInline):
    model = CustomPageMember
    form = CustomPageMemberForm
    extra = 1
    fields = ('name', 'designation', 'role', 'photo', 'email', 'phone', 'order')


class CustomPageActivityInline(admin.TabularInline):
    model = CustomPageActivity
    form = CustomPageActivityForm
    extra = 1
    fields = ('title', 'description', 'date', 'attachment', 'image', 'order')


class CustomPageEventLinkInline(admin.TabularInline):
    model = CustomPageEventLink
    form = CustomPageEventLinkForm
    extra = 1
    fields = ('happening', 'order')


class CustomPageGalleryImageInline(admin.TabularInline):
    model = CustomPageGalleryImage
    form = CustomPageGalleryImageForm
    extra = 1
    fields = ('image', 'caption', 'order')


@admin.register(CustomPage)
class CustomPageAdmin(admin.ModelAdmin):
    form = CustomPageForm
    list_display = ('title', 'slug', 'get_full_url', 'order', 'updated_at')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'slug')
    inlines = [
        CustomPageSlideInline, 
        CustomPageMemberInline, 
        CustomPageActivityInline, 
        CustomPageEventLinkInline, 
        CustomPageGalleryImageInline
    ]
    
    fieldsets = (
        ('Basic Configuration', {'fields': ('title', 'slug', 'order')}),
        ('Content Section', {'fields': ('description',)}),
        ('Section Toggles (On/Off)', {
            'fields': ('show_slider', 'show_members', 'show_activities', 'show_events', 'show_gallery'),
            'description': 'Toggle visibility of dynamic components on this page.'
        }),
    )

    def get_full_url(self, obj):
        url = reverse('custom_pages:custom_page_detail', kwargs={'slug': obj.slug})
        return format_html('<a href="{0}" target="_blank" style="font-weight: bold; color: #E61013;">http://127.0.0.1:8000{0}</a>', url)
    get_full_url.short_description = 'Page URL (View Page)'
