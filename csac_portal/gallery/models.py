from django.db import models
import os


def gallery_item_upload_path(instance, filename):
    """
    Saves files to separate folders depending on the selected gallery type:
    - Image: gallery/images/
    - News: gallery/news/
    - Video/Media: gallery/videos/
    """
    g_type = getattr(instance, 'gallery_type', 'image')
    if g_type == 'news':
        return os.path.join('gallery', 'news', filename)
    elif g_type == 'video':
        return os.path.join('gallery', 'videos', filename)
    return os.path.join('gallery', 'images', filename)


class GalleryCategory(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Gallery Category"
        verbose_name_plural = "Gallery Categories"

    def __str__(self):
        return self.name


class GalleryItem(models.Model):
    TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video/Media'),
        ('news', 'News'),
    ]
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, related_name='items')
    gallery_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='image')
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=gallery_item_upload_path, blank=True)
    image_url = models.URLField(blank=True, help_text="External image URL (S3 etc.)")
    video_url = models.URLField(blank=True, help_text="YouTube or other video URL")
    news_source = models.CharField(max_length=200, blank=True)
    date = models.DateField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_homepage_highlight = models.BooleanField(
        default=False,
        verbose_name="Is Homepage Highlight",
        help_text="Check to display this gallery item in the homepage popup highlights section."
    )
    highlight_subtitle = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Highlight Subtitle",
        help_text="Optional subtitle/caption details for the homepage highlight popup."
    )

    class Meta:
        ordering = ['order', '-date']
        verbose_name = "Gallery Item"

    def __str__(self):
        return self.title

    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url

    def get_video_thumbnail(self):
        # 1. Check if the admin uploaded a custom cover/thumbnail image
        custom_image = self.get_image()
        if custom_image:
            return custom_image

        # 2. Fallback to automatic YouTube thumbnail
        if self.gallery_type == 'video' and self.video_url:
            import re
            patterns = [
                r'v=([a-zA-Z0-9_-]{11})',
                r'shorts/([a-zA-Z0-9_-]{11})',
                r'youtu\.be/([a-zA-Z0-9_-]{11})',
                r'embed/([a-zA-Z0-9_-]{11})',
            ]
            for pattern in patterns:
                match = re.search(pattern, self.video_url)
                if match:
                    return f"https://img.youtube.com/vi/{match.group(1)}/hqdefault.jpg"
        return ""

    def get_embed_url(self):
        """Extracts YouTube ID and builds embed URL with autoplay."""
        if self.gallery_type == 'video' and self.video_url:
            import re
            patterns = [
                r'v=([a-zA-Z0-9_-]{11})',
                r'shorts/([a-zA-Z0-9_-]{11})',
                r'youtu\.be/([a-zA-Z0-9_-]{11})',
                r'embed/([a-zA-Z0-9_-]{11})',
            ]
            for pattern in patterns:
                match = re.search(pattern, self.video_url)
                if match:
                    return f"https://www.youtube.com/embed/{match.group(1)}?autoplay=1"
        return ""
