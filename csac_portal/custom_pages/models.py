from django.db import models
from django.urls import reverse
from core.models import Happening
from django_ckeditor_5.fields import CKEditor5Field


class CustomPage(models.Model):
    title = models.CharField(max_length=200, help_text="Title of the custom page")
    slug = models.SlugField(unique=True, max_length=200, help_text="Unique URL path (e.g., science-club)")
    description = CKEditor5Field('Description', config_name='extends', blank=True, help_text="Main description/introduction text (supports HTML)")
    
    # Section Toggles
    show_slider = models.BooleanField(default=True, verbose_name="Show Image Slider")
    show_members = models.BooleanField(default=False, verbose_name="Show Member Listing")
    show_activities = models.BooleanField(default=False, verbose_name="Show Activities")
    show_events = models.BooleanField(default=False, verbose_name="Show Events (Imported from Happenings)")
    show_gallery = models.BooleanField(default=False, verbose_name="Show Gallery Grid")
    
    order = models.PositiveIntegerField(default=0, help_text="Sorting order in navigation/lists")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Custom Page"
        verbose_name_plural = "Custom Pages"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('custom_pages:custom_page_detail', kwargs={'slug': self.slug})


class CustomPageSlide(models.Model):
    page = models.ForeignKey(CustomPage, on_delete=models.CASCADE, related_name='slides')
    image = models.ImageField(upload_to='custom_pages/slides/')
    caption = models.CharField(max_length=250, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Custom Page Slider Image"
        verbose_name_plural = "Custom Page Slider Images"

    def __str__(self):
        return f"Slide {self.id} for {self.page.title}"


class CustomPageMember(models.Model):
    page = models.ForeignKey(CustomPage, on_delete=models.CASCADE, related_name='members')
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    role = models.CharField(max_length=150, blank=True, help_text="e.g. Coordinator, Committee Head, Member")
    photo = models.ImageField(upload_to='custom_pages/members/', blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Custom Page Member"
        verbose_name_plural = "Custom Page Members"

    def __str__(self):
        return f"{self.name} - {self.page.title}"


class CustomPageActivity(models.Model):
    page = models.ForeignKey(CustomPage, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=300)
    description = CKEditor5Field('Description', config_name='extends', blank=True)
    date = models.DateField(blank=True, null=True)
    attachment = models.FileField(upload_to='custom_pages/attachments/', blank=True, help_text="Upload a PDF or document attachment")
    image = models.ImageField(upload_to='custom_pages/activities/', blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-date']
        verbose_name = "Custom Page Activity"
        verbose_name_plural = "Custom Page Activities"

    def __str__(self):
        return self.title


class CustomPageEventLink(models.Model):
    page = models.ForeignKey(CustomPage, on_delete=models.CASCADE, related_name='events')
    happening = models.ForeignKey(Happening, on_delete=models.CASCADE, verbose_name="Happening / Event", help_text="Select a Happening to display on this page")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-happening__date']
        verbose_name = "Custom Page Linked Event"
        verbose_name_plural = "Custom Page Linked Events"

    def __str__(self):
        return f"{self.happening.title} Linked to {self.page.title}"


class CustomPageGalleryImage(models.Model):
    page = models.ForeignKey(CustomPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='custom_pages/gallery/')
    caption = models.CharField(max_length=250, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Custom Page Gallery Image"
        verbose_name_plural = "Custom Page Gallery Images"

    def __str__(self):
        return f"Gallery Image {self.id} for {self.page.title}"
