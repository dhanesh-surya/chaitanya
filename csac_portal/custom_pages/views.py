from django.shortcuts import render, get_object_or_404
from .models import CustomPage

def custom_page_detail(request, slug):
    # Fetch CustomPage and prefetch all related elements to optimize DB queries
    page = get_object_or_404(
        CustomPage.objects.prefetch_related(
            'slides',
            'members',
            'activities',
            'events__happening',
            'gallery_images'
        ),
        slug=slug
    )
    context = {
        'page': page,
        'page_title': page.title,
        'breadcrumb': page.title,
    }
    return render(request, 'custom_pages/custom_page_detail.html', context)
