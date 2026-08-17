from django.shortcuts import render
from .models import GalleryCategory, GalleryItem


def image_gallery(request):
    categories = GalleryCategory.objects.filter(items__gallery_type='image', items__is_active=True).distinct()
    items = GalleryItem.objects.filter(gallery_type='image', is_active=True)
    context = {
        'categories': categories,
        'items': items,
        'page_title': 'Image Gallery',
        'breadcrumb': 'Image Gallery',
    }
    return render(request, 'gallery/image_gallery.html', context)


def video_gallery(request):
    categories = GalleryCategory.objects.filter(items__gallery_type='video', items__is_active=True).distinct()
    items = GalleryItem.objects.filter(gallery_type='video', is_active=True)
    context = {
        'categories': categories,
        'items': items,
        'page_title': 'Video Gallery',
        'breadcrumb': 'Video Gallery',
    }
    return render(request, 'gallery/video_gallery.html', context)


def news_gallery(request):
    categories = GalleryCategory.objects.filter(items__gallery_type='news', items__is_active=True).distinct()
    items = GalleryItem.objects.filter(gallery_type='news', is_active=True)
    context = {
        'categories': categories,
        'items': items,
        'page_title': 'News Gallery',
        'breadcrumb': 'News Gallery',
    }
    return render(request, 'gallery/news_gallery.html', context)
