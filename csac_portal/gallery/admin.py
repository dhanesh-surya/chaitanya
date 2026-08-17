from django.contrib import admin
from .models import GalleryCategory, GalleryItem
from .forms import GalleryItemForm


class GalleryItemInline(admin.TabularInline):
    model = GalleryItem
    form = GalleryItemForm
    extra = 1
    fields = ('gallery_type', 'title', 'image', 'image_url', 'video_url', 'date', 'order', 'is_active')


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
    inlines = [GalleryItemInline]


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    form = GalleryItemForm
    list_display = ('title', 'category', 'gallery_type', 'date', 'order', 'is_active')
    list_filter = ('gallery_type', 'category', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')
