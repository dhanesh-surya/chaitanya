from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field


class SiteSettings(models.Model):
    college_name_en = models.CharField(max_length=200, default="Chaitanya Science and Arts College")
    college_name_hi = models.CharField(max_length=200, default="चैतन्य विज्ञान एवं कला महाविद्यालय, पामगढ़")
    tagline = models.CharField(max_length=300, default="An Autonomous College, Approved by UGC | Accredited with Grade 'A' by NAAC")
    address_line1 = models.CharField(max_length=200, default="PAMGARH, JANJGIR-CHAMPA (C.G.), 495554")
    address_line2 = models.CharField(max_length=200, default="Affiliated to Shaheed Nandkumar Patel Vishwavidyalaya, Raigarh")
    phone = models.CharField(max_length=20, default="+91-9425540666")
    email = models.EmailField(default="chaitanyapamgarh@gmail.com")
    facebook_url = models.URLField(blank=True, default="https://www.facebook.com/ChaitanyaPamgarh/")
    youtube_url = models.URLField(blank=True, default="https://www.youtube.com/@ChaitanyaCollegePamgarh")
    instagram_url = models.URLField(blank=True)
    google_maps_embed = models.TextField(blank=True)
    established_year = models.IntegerField(default=2001)

    # Style fields for college_name_en
    college_name_en_font_family = models.CharField(max_length=100, default="Roboto Slab", verbose_name="College Name (EN) Font Family")
    college_name_en_google_font_url = models.URLField(blank=True, verbose_name="College Name (EN) Google Font Link", help_text="Google Fonts stylesheet URL")
    college_name_en_font_size = models.CharField(max_length=50, default="24px", verbose_name="College Name (EN) Font Size")
    college_name_en_font_color = models.CharField(max_length=20, default="#E61013", verbose_name="College Name (EN) Font Color")

    # Style fields for college_name_hi
    college_name_hi_font_family = models.CharField(max_length=100, default="Roboto Slab", verbose_name="College Name (HI) Font Family")
    college_name_hi_google_font_url = models.URLField(blank=True, verbose_name="College Name (HI) Google Font Link", help_text="Google Fonts stylesheet URL")
    college_name_hi_font_size = models.CharField(max_length=50, default="24px", verbose_name="College Name (HI) Font Size")
    college_name_hi_font_color = models.CharField(max_length=20, default="#E61013", verbose_name="College Name (HI) Font Color")

    # Style fields for tagline
    tagline_font_family = models.CharField(max_length=100, default="Roboto Slab", verbose_name="Tagline Font Family")
    tagline_google_font_url = models.URLField(blank=True, verbose_name="Tagline Google Font Link", help_text="Google Fonts stylesheet URL")
    tagline_font_size = models.CharField(max_length=50, default="16px", verbose_name="Tagline Font Size")
    tagline_font_color = models.CharField(max_length=20, default="#E61013", verbose_name="Tagline Font Color")

    # Style fields for address_line1
    address_line1_font_family = models.CharField(max_length=100, default="Roboto Slab", verbose_name="Address Line 1 Font Family")
    address_line1_google_font_url = models.URLField(blank=True, verbose_name="Address Line 1 Google Font Link", help_text="Google Fonts stylesheet URL")
    address_line1_font_size = models.CharField(max_length=50, default="20px", verbose_name="Address Line 1 Font Size")
    address_line1_font_color = models.CharField(max_length=20, default="#000000", verbose_name="Address Line 1 Font Color")

    # Style fields for address_line2
    address_line2_font_family = models.CharField(max_length=100, default="Roboto Slab", verbose_name="Address Line 2 Font Family")
    address_line2_google_font_url = models.URLField(blank=True, verbose_name="Address Line 2 Google Font Link", help_text="Google Fonts stylesheet URL")
    address_line2_font_size = models.CharField(max_length=50, default="16px", verbose_name="Address Line 2 Font Size")
    address_line2_font_color = models.CharField(max_length=20, default="#000000", verbose_name="Address Line 2 Font Color")

    # Logo fields
    college_logo = models.ImageField(upload_to='logos/', blank=True, null=True, verbose_name="College Logo (Header/Footer)")
    college_logo_mobile = models.ImageField(upload_to='logos/', blank=True, null=True, verbose_name="Mobile Logo")
    logo2 = models.ImageField(upload_to='logos/', blank=True, null=True, verbose_name="Logo 2 (NAAC A)")
    logo3 = models.ImageField(upload_to='logos/', blank=True, null=True, verbose_name="Logo 3")
    logo4 = models.ImageField(upload_to='logos/', blank=True, null=True, verbose_name="Logo 4")
    logo5 = models.ImageField(upload_to='logos/', blank=True, null=True, verbose_name="Logo 5")

    # Header Image Layout fields
    use_image_header = models.BooleanField(default=False, verbose_name="Use Image Header", help_text="Check this to display the custom header image banner instead of the default text and logos.")
    header_image = models.ImageField(upload_to='headers/', blank=True, null=True, verbose_name="Header Image (Banner)", help_text="Upload a custom header image banner. This will replace the text header and logos if 'Use Image Header' is checked.")

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.college_name_en

    def get_college_logo(self):
        if self.college_logo:
            return self.college_logo.url
        from django.templatetags.static import static
        return static('assets/csac_pmg.svg')

    def get_logo2(self):
        if self.logo2:
            return self.logo2.url
        from django.templatetags.static import static
        return static('assets/images/logo_naac_a.png')

    def get_logo3(self):
        if self.logo3:
            return self.logo3.url
        from django.templatetags.static import static
        return static('assets/images/logo_2.png')

    def get_logo4(self):
        if self.logo4:
            return self.logo4.url
        from django.templatetags.static import static
        return static('assets/images/logo_3.png')

    def get_logo5(self):
        if self.logo5:
            return self.logo5.url
        from django.templatetags.static import static
        return static('assets/images/logo_4.png')

    def get_mobile_logo(self):
        if self.college_logo_mobile:
            return self.college_logo_mobile.url
        from django.templatetags.static import static
        return static('assets/csac_mobile.svg')


class BannerSlide(models.Model):
    caption = models.CharField(max_length=300)
    image = models.ImageField(upload_to='banner/', blank=True)
    image_url = models.URLField(blank=True, help_text="Use this for external S3 URLs if no local image")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.caption

    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url


class AccreditationLogo(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='accreditation/', blank=True)
    image_url = models.URLField(blank=True)
    link = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_image(self):
        return self.image.url if self.image else self.image_url


class StatCounter(models.Model):
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=20, help_text="e.g. 8000+")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.value} - {self.label}"


class CollegeInfo(models.Model):
    """About section text blocks"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    section = models.CharField(max_length=50, choices=[
        ('about', 'About'),
        ('vision', 'Vision'),
        ('mission', 'Mission'),
        ('governance', 'Governance'),
        ('features', 'Distinctive Features'),
    ])
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "College Info Section"

    def __str__(self):
        return f"{self.section} - {self.title}"


class Leadership(models.Model):
    ROLE_CHOICES = [
        ('principal', 'Principal'),
        ('director', 'Director/Founder'),
        ('vice_principal', 'Vice Principal'),
        ('chairman', 'Chairman'),
    ]
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    qualification = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True, help_text="Email address shown on the home and about pages")
    photo = models.ImageField(upload_to='leadership/', blank=True)
    message = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"

    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        if self.role == 'principal':
            return 'https://chaitanyafiles01.s3.amazonaws.com/aboutImages/vkgupta.png'
        return 'https://chaitanyafiles01.s3.amazonaws.com/directorImages/DSC_0086.JPG'


class Committee(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=250, blank=True, null=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class CommitteeMember(models.Model):
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name='members')
    name = models.CharField(max_length=150)
    designation = models.CharField(max_length=200)
    role_in_committee = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class CommitteeActivity(models.Model):
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    date = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='committees/activities/', blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-date']
        verbose_name = "Committee Activity"
        verbose_name_plural = "Committee Activities"

    def __str__(self):
        return f"{self.committee.name} - {self.title}"


class CommitteeGalleryImage(models.Model):
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='committees/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Committee Gallery Image"
        verbose_name_plural = "Committee Gallery Images"

    def __str__(self):
        return f"Gallery Image for {self.committee.name}"



class Policy(models.Model):
    title = models.CharField(max_length=200)
    document = models.FileField(upload_to='policies/', blank=True)
    document_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Policies"

    def __str__(self):
        return self.title


class Achievement(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='achievements/', blank=True)
    image_url = models.URLField(blank=True)
    year = models.IntegerField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-year', 'order']

    def __str__(self):
        return self.title


class Notice(models.Model):
    CATEGORY_CHOICES = [
        ('latest', 'Latest'),
        ('exam', 'Exam'),
        ('admission', 'Admission'),
        ('students', 'Students'),
        ('sports', 'Sports'),
    ]
    title = models.CharField(max_length=300)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='latest')
    document = models.FileField(upload_to='notices/', blank=True)
    document_url = models.URLField(blank=True)
    published_date = models.DateField(default=timezone.now)
    show_in_marquee = models.BooleanField(default=False, verbose_name="Show in Marquee")
    marquee_flag = models.CharField(max_length=50, blank=True, null=True, verbose_name="Marquee Flag (Optional)", help_text="Custom text to highlight in the marquee (e.g. 'NEW', 'URGENT')")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"


class ImportantLink(models.Model):
    name = models.CharField(max_length=150)
    url = models.URLField()
    category = models.CharField(max_length=50, choices=[
        ('important', 'Important Links'),
        ('quick', 'Quick Links'),
    ], default='important')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class CareerGuidanceSubmission(models.Model):
    fname = models.CharField(max_length=100, verbose_name="First Name")
    lname = models.CharField(max_length=100, verbose_name="Last Name")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Phone")
    msg = models.TextField(verbose_name="Message/Comments")
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Career Guidance Submission"

    def __str__(self):
        return f"{self.fname} {self.lname} - {self.email}"


class SocialScheme(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100) # e.g. "Women Education"
    description = models.TextField()
    image = models.ImageField(upload_to='social_schemes/', blank=True)
    image_url = models.URLField(blank=True)
    link = models.CharField(max_length=200, blank=True, help_text="e.g. social-schemes/1/index.html")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Social Scheme"

    def __str__(self):
        return self.title

    def get_image(self):
        return self.image.url if self.image else self.image_url


class Testimonial(models.Model):
    student_name = models.CharField(max_length=150)
    program = models.CharField(max_length=150, help_text="e.g. M.Sc. Zoology (2022-23)")
    rating = models.PositiveIntegerField(default=5, help_text="1 to 5 stars")
    text = models.TextField()
    photo = models.ImageField(upload_to='testimonials/', blank=True)
    photo_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'student_name']

    def __str__(self):
        return self.student_name

    def get_photo(self):
        return self.photo.url if self.photo else self.photo_url


class Event(models.Model):
    title = models.CharField(max_length=300)
    date = models.DateField()
    time = models.CharField(max_length=50, blank=True) # e.g. "11 a.m."
    location = models.CharField(max_length=200, default="College Auditorium")
    image = models.ImageField(upload_to='events/', blank=True, null=True, help_text="Upload event brochure/poster (300x200px recommended)")
    image_url = models.URLField(blank=True, help_text="External URL for brochure/poster if not uploaded locally")
    link = models.URLField(blank=True)
    description = CKEditor5Field('Description', config_name='extends', blank=True, help_text="Detailed description of the upcoming event")
    brochure = models.FileField(upload_to='events/brochures/', blank=True, null=True, help_text="Upload event brochure or registration details (PDF)")
    registration_link = models.URLField(blank=True, max_length=500, help_text="External URL for online registration (e.g. Google Form)")
    youtube_url = models.URLField(blank=True, max_length=500, help_text="Optional YouTube video URL (watch link or short link)")
    is_active = models.BooleanField(default=True)
    is_sports_event = models.BooleanField(
        default=False,
        verbose_name="Is Sports Event",
        help_text="Check to show this event in the Sports page Upcoming Events section"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title

    def get_image(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        from django.templatetags.static import static
        return static('assets/images/feature/admission.jpg')

    def get_youtube_embed_url(self):
        if not self.youtube_url:
            return None
        import re
        regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
        match = re.search(regex, self.youtube_url)
        if match:
            video_id = match.group(1)
            return f"https://www.youtube-nocookie.com/embed/{video_id}"
        return self.youtube_url


class Happening(models.Model):
    title = models.CharField(max_length=300)
    category = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to='happenings/', blank=True)
    image_url = models.URLField(blank=True, max_length=500)
    link = models.CharField(max_length=200, blank=True, help_text="e.g. /event-details/148/index.html")
    date = models.DateField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    
    # New fields
    department = models.ForeignKey(
        'academics.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='happenings',
        verbose_name="Department"
    )
    description = CKEditor5Field('Description', config_name='extends', blank=True)
    participants_count = models.PositiveIntegerField(blank=True, null=True, verbose_name="Number of Participants")
    brochure = models.FileField(upload_to='happenings/brochures/', blank=True, null=True, help_text="Upload brochure or registration form (PDF)")
    registration_link = models.URLField(blank=True, max_length=500, help_text="Link for registration (Google Form etc.)")
    banner_image_url = models.URLField(blank=True, max_length=500, help_text="Custom header banner image URL")
    is_nss_activity = models.BooleanField(default=False, verbose_name="Is NSS Activity", help_text="Check if this event/happening is part of NSS activities and should appear in the NSS page slider")
    is_iic_activity = models.BooleanField(default=False, verbose_name="Is IIC Activity", help_text="Check if this event/happening is part of IIC activities and should appear in the IIC page slider")
    is_sports_activity = models.BooleanField(default=False, verbose_name="Is Sports Activity", help_text="Check if this event/happening is a sports activity and should appear in the Sports page")

    class Meta:
        ordering = ['order', '-date']
        verbose_name = "Happening"

    def __str__(self):
        return self.title

    def get_image(self):
        return self.image.url if self.image else self.image_url


class HappeningImage(models.Model):
    happening = models.ForeignKey(Happening, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='happenings/gallery/', blank=True)
    image_url = models.URLField(blank=True, max_length=500, help_text="External URL for image if not uploaded locally")
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Happening Gallery Image"
        verbose_name_plural = "Happening Gallery Images"

    def __str__(self):
        return f"Gallery Image for {self.happening.title}"

    def get_image(self):
        return self.image.url if self.image else self.image_url


class QuickLinkCard(models.Model):
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=200, help_text="e.g. 'students:merit_list' (Django name) or a relative path '/about/'")
    icon = models.FileField(upload_to='icons/', blank=True, null=True, help_text="Upload custom SVG/PNG icon. Falls back to 07.svg.")
    icon_url = models.URLField(blank=True)
    fa_icon = models.CharField(max_length=100, blank=True, help_text="FontAwesome icon class name, e.g. 'fa-graduation-cap', 'fa-building', 'fa-book-open'")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # Custom design fields
    bg_color = models.CharField(max_length=7, default="#ffffff", help_text="HEX color for card background, e.g. #ffffff or #B71A34")
    bg_image = models.ImageField(upload_to='cards/', blank=True, null=True, help_text="Upload custom background image for the card.")
    overlay_color = models.CharField(max_length=7, default="#000000", help_text="HEX color for background overlay, e.g. #000000")
    overlay_opacity = models.FloatField(default=0.0, help_text="Overlay opacity between 0.0 (fully transparent) and 1.0 (fully opaque)")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Quick Link Card"
        verbose_name_plural = "Quick Link Cards"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse, NoReverseMatch
        try:
            return reverse(self.link)
        except NoReverseMatch:
            return self.link

    def get_icon(self):
        if self.icon:
            return self.icon.url
        if self.icon_url:
            return self.icon_url
        from django.templatetags.static import static
        return static('assets/images/icon/07.svg')


class AboutPage(models.Model):
    # Header & Breadcrumb
    page_title = models.CharField(max_length=200, default="About Chaitanya Science and Arts College")
    breadcrumb_image = models.ImageField(
        upload_to='breadcrumbs/about/',
        blank=True, null=True,
        verbose_name="Breadcrumb Background Image",
        help_text="Upload a custom breadcrumb banner image for the About page."
    )
    breadcrumb_image_url = models.URLField(
        blank=True,
        verbose_name="Breadcrumb Image URL (External)",
        help_text="Use an external URL if not uploading a local image. Leave blank to use theme default."
    )

    # About Us Section
    about_us_title = models.CharField(max_length=200, default="About Us")
    about_us_description_1 = CKEditor5Field('About Us Description 1', config_name='extends', blank=True, default="")
    about_us_description_2 = CKEditor5Field('About Us Description 2', config_name='extends', blank=True, default="")
    about_us_description_3 = CKEditor5Field('About Us Description 3', config_name='extends', blank=True, default="")
    about_us_image_url = models.CharField(max_length=500, default="https://chaitanyafiles01.s3.amazonaws.com/aboutImages/COLLEGE_BUILDING.jpg")
    about_us_image = models.ImageField(
        upload_to='about/',
        blank=True, null=True,
        verbose_name="About Us Main Image",
        help_text="Upload a local image file to display in the main About Us section."
    )

    # Stats next to image
    stat1_value = models.CharField(max_length=50, default="8000+")
    stat1_label = models.CharField(max_length=150, default="Undergradute & Graduate Students")
    stat1_icon = models.CharField(max_length=150, default="assets/images/icon/11.svg")

    stat2_value = models.CharField(max_length=50, default="50+")
    stat2_label = models.CharField(max_length=150, default="Chaitanya College Faculty and Staff")
    stat2_icon = models.CharField(max_length=150, default="assets/images/icon/12.svg")

    stat3_value = models.CharField(max_length=50, default="5000+")
    stat3_label = models.CharField(max_length=150, default="Chaitanya College Alumni Worldwide")
    stat3_icon = models.CharField(max_length=150, default="assets/images/icon/13.svg")

    # Fun facts in the red bar
    funfact1_value = models.CharField(max_length=50, default="90%")
    funfact1_label = models.CharField(max_length=150, default="Graduate success rate")

    funfact2_value = models.CharField(max_length=50, default="Top 10")
    funfact2_label = models.CharField(max_length=150, default="Colleges in CG that Create Futures")

    funfact3_value = models.CharField(max_length=50, default="No. 1")
    funfact3_label = models.CharField(max_length=150, default="In Innovation & Entrepreneurship")

    # Vision & Mission
    mission_statement = CKEditor5Field('Mission Statement', config_name='extends', blank=True, default="")
    vision_title = models.CharField(max_length=100, default="Vision")
    vision_text = CKEditor5Field('Vision Text', config_name='extends', blank=True, default="")
    mission_title = models.CharField(max_length=100, default="Mission")
    mission_text_1 = CKEditor5Field('Mission Text 1', config_name='extends', blank=True, default="")
    mission_text_2 = CKEditor5Field('Mission Text 2', config_name='extends', blank=True, default="")

    # Governance
    governance_title = models.CharField(max_length=200, default="Governance")
    governance_text = CKEditor5Field('Governance Text', config_name='extends', blank=True, default="")

    # Distinctive Features
    features_title = models.CharField(max_length=200, default="Distinctive Features of the College")
    features_list = models.TextField(help_text="Enter distinctive features, one per line", default="")

    # Testimonial
    testimonial_text = CKEditor5Field('Testimonial Text', config_name='extends', blank=True, default="")
    testimonial_author = models.CharField(max_length=150, default="VK Gupta")
    testimonial_author_image = models.ImageField(upload_to='about/', blank=True, null=True)

    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Page"

    def __str__(self):
        return self.page_title

    def get_about_us_image(self):
        if self.about_us_image:
            return self.about_us_image.url
        return self.about_us_image_url

    def get_breadcrumb_image(self):
        """Returns the breadcrumb image URL: uploaded file > external URL > empty."""
        if self.breadcrumb_image:
            return self.breadcrumb_image.url
        return self.breadcrumb_image_url or ''


class Recognition(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='recognition/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Recognition Document"
        verbose_name_plural = "Recognition Documents"

    def __str__(self):
        return self.title


class UGCTable(models.Model):
    name = models.CharField(max_length=200, help_text="Name of the custom table (e.g. UGC Files, Autonomy Grant Documents)")
    order = models.PositiveIntegerField(default=0, help_text="Sorting order of tables on the UGC page")
    is_active = models.BooleanField(default=True, help_text="Toggle table visibility on the front end")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "UGC Table"
        verbose_name_plural = "UGC Tables"

    def __str__(self):
        return self.name


class UGCDocument(models.Model):
    ugc_table = models.ForeignKey(UGCTable, on_delete=models.CASCADE, related_name='documents', help_text="Select the table this document belongs to")
    sn = models.PositiveIntegerField(default=1, verbose_name="S.N.", help_text="Serial number inside the table")
    title = models.CharField(max_length=300, verbose_name="Name of the file/document")
    file = models.FileField(upload_to='ugc/documents/', blank=True, null=True, help_text="Upload local PDF/document")
    file_url = models.URLField(blank=True, max_length=500, help_text="External URL link (if not uploading local file)")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sn', 'id']
        verbose_name = "UGC Document"
        verbose_name_plural = "UGC Documents"

    def __str__(self):
        return f"[{self.ugc_table.name}] {self.title}"

    def get_file_url(self):
        if self.file:
            return self.file.url
        return self.file_url


class UGCPageSettings(models.Model):
    heading = models.CharField(max_length=200, default="University Grants Commission (UGC) Recognition")
    description = models.TextField(default="Chaitanya Science and Arts College is recognized under Sections 2(f) and 12(B) of the UGC Act, 1956. This recognition establishes our credibility as a premier institution of higher learning eligible for central assistance and academic development programs. The college is committed to maintaining high standards of education, research, and infrastructure as mandated by the UGC.")
    
    # Show/hide controls
    show_ugc_details = models.BooleanField(default=True, verbose_name="Show UGC Details Cards", help_text="Check to show the Autonomy, 2(f)/12(B), and Autonomy Benefits cards section")
    
    # Autonomy Card
    autonomy_status_title = models.CharField(max_length=150, default="Autonomous")
    autonomy_status_subtitle = models.CharField(max_length=150, default="UGC Autonomous Status")
    autonomy_status_text = models.TextField(default="Empowered to design its own curriculum, conduct examinations, and evaluate student performance.")
    
    # 2(f)/12(B) Card
    status_2f_12b_title = models.CharField(max_length=150, default="2(f) and 12(B) Status")
    status_2f_12b_text = models.TextField(default="The recognition under Section 2(f) signifies that our college is a recognized higher education institution.\n\nThe Section 12(B) status makes the college eligible to receive developmental grants from the UGC and other central agencies for teaching, research, and infrastructure upgrades.")
    
    # Autonomy Benefits Card
    benefits_title = models.CharField(max_length=150, default="Autonomy Benefits")
    benefits_list = models.TextField(default="Modernized, industry-relevant curriculum.\nChoice-Based Credit System (CBCS).\nFaster result processing and publication.\nFocus on skill-based and vocational courses.", help_text="Enter one benefit per line")
    
    # Grants Section
    show_grants_section = models.BooleanField(default=True, verbose_name="Show UGC & Central Funding Support Table", help_text="Check to show the UGC & Central Funding Support grants table")
    grants_title = models.CharField(max_length=200, default="UGC & Central Funding Support")

    class Meta:
        verbose_name = "UGC Page Settings"
        verbose_name_plural = "UGC Page Settings"

    def __str__(self):
        return "UGC Page Settings"


class UGCGrant(models.Model):
    scheme = models.CharField(max_length=200, verbose_name="Scheme / Funding Agency")
    purpose = models.CharField(max_length=300, verbose_name="Purpose of Grant")
    impact = models.CharField(max_length=300, verbose_name="Impact & Upgrades")
    order = models.PositiveIntegerField(default=0, help_text="Sorting order of rows in the table")
    is_active = models.BooleanField(default=True, verbose_name="Show in Table", help_text="Uncheck to hide this row from the table")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "UGC Grant / Funding Record"
        verbose_name_plural = "UGC Grant / Funding Records"

    def __str__(self):
        return f"{self.scheme} - {self.purpose[:50]}"


class PopupAnnouncement(models.Model):
    title = models.CharField(max_length=200, help_text="Title of the announcement (for internal identification)")
    image = models.ImageField(upload_to='popup_announcements/', blank=True, null=True, help_text="Upload a poster/image for the popup")
    image_url = models.URLField(blank=True, help_text="Or enter an external image URL if no local file is uploaded")
    text = CKEditor5Field('Announcement Content', config_name='extends', blank=True, help_text="Custom rich text details shown inside the modal")
    link = models.URLField(blank=True, help_text="Optional custom link to redirect users (e.g., Admission page)")
    link_text = models.CharField(max_length=100, default="Learn More", help_text="Action button label")
    is_active = models.BooleanField(default=False, help_text="Check to display this announcement in the popup list on the homepage")
    show_once_per_session = models.BooleanField(default=True, help_text="If checked, the popup will only display once per browser session. Otherwise, it will show on every homepage load.")
    order = models.PositiveIntegerField(default=0, help_text="Display order in the popup list (lower numbers appear first)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Popup Announcement"
        verbose_name_plural = "Popup Announcements"
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url




class BreadcrumbSettings(models.Model):
    """
    Singleton model — holds the site-wide default breadcrumb background image.
    Only one row should ever exist. Controlled via the singleton guard in admin.
    """
    default_image = models.ImageField(
        upload_to='breadcrumbs/',
        blank=True, null=True,
        verbose_name="Default Background Image",
        help_text="Upload the default breadcrumb banner image used across all pages."
    )
    default_image_url = models.URLField(
        blank=True,
        verbose_name="Default Image URL (External)",
        help_text="Use an external URL if you are not uploading a local image."
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Enable Per-Page Overrides",
        help_text="When checked, per-page breadcrumb overrides can replace the global default. "
                  "When unchecked, all pages use only the global default image above."
    )

    class Meta:
        verbose_name = "Breadcrumb Settings (Global Default)"
        verbose_name_plural = "Breadcrumb Settings (Global Default)"

    def __str__(self):
        return "Global Breadcrumb Settings"

    def get_image(self):
        """Returns the resolved URL for the default image, or empty string."""
        if self.default_image:
            return self.default_image.url
        return self.default_image_url or ''


class PageBreadcrumb(models.Model):
    """
    Per-page breadcrumb image override.
    Each row targets one specific page via page_key.
    """
    PAGE_KEY_CHOICES = [
        # Core app
        ('about',                    'About Us'),
        ('committees',               'Committees'),
        ('committee_detail',         'Committee Detail'),
        ('policies',                 'Policies'),
        ('recognition',              'Achievements & Recognition'),
        ('staff_teaching',           'Teaching Staff'),
        ('staff_nonteaching',        'Non-Teaching Staff'),
        ('notices',                  'Notice Board'),
        ('contact',                  'Contact Us'),
        ('nss',                      'NSS'),
        ('iic',                      'IIC'),
        ('ugc',                      'UGC'),
        ('nep',                      'NEP 2020'),
        ('sports',                   'Sports'),
        ('co_po',                    'CO PO'),
        ('happenings',               'Recent Happenings'),
        ('happening_detail',         'Happening Detail'),
        ('event_detail',             'Event Detail'),
        # Academics
        ('academics_programs',       'Programs Offered'),
        ('academics_calendar',       'Academic Calendar'),
        ('academics_dept_detail',    'Department Detail'),
        # Students
        ('students_admission',       'Admission Procedure'),
        ('students_online_admission','Online Admission'),
        ('students_fee_structure',   'Fee Structure'),
        ('students_scholarship',     'Scholarship'),
        ('students_library',         'Library'),
        ('students_alumni',          'Alumni'),
        ('students_merit_list',      'Merit List'),
        ('students_syllabus',        'Syllabus'),
        # NAAC
        ('naac_home',                'NAAC'),
        ('naac_iqac',                'IQAC'),
        ('naac_iiqa',                'IIQA'),
        ('naac_ssr',                 'SSR'),
        ('naac_dvv',                 'DVV'),
        ('naac_atr',                 'ATR'),
        # Gallery
        ('gallery_images',           'Image Gallery'),
        ('gallery_videos',           'Video Gallery'),
        ('gallery_news',             'News Gallery'),
        # Feedback
        ('feedback_student',         'Student Feedback'),
        ('feedback_parent',          'Parent Feedback'),
        ('feedback_faculty',         'Faculty Feedback'),
        ('feedback_alumni',          'Alumni Feedback'),
        # Grievances
        ('grievances_anti_ragging',  'Anti Ragging Committee'),
        ('grievances_icc',           'Internal Complaints Committee (ICC)'),
        ('grievances_redressal',     'Grievance Redressal'),
        ('grievances_submit',        'Submit a Grievance'),
        # Custom pages
        ('custom_page',              'Custom Page'),
        ('infrastructure',           'Infrastructure'),
    ]

    page_key = models.CharField(
        max_length=60,
        choices=PAGE_KEY_CHOICES,
        unique=True,
        verbose_name="Page",
        help_text="Select the page this breadcrumb image applies to."
    )
    custom_image = models.ImageField(
        upload_to='breadcrumbs/pages/',
        blank=True, null=True,
        verbose_name="Custom Background Image",
        help_text="Upload a custom breadcrumb banner image for this specific page."
    )
    custom_image_url = models.URLField(
        blank=True,
        verbose_name="Custom Image URL (External)",
        help_text="Use an external URL for the image if not uploading locally."
    )
    use_default = models.BooleanField(
        default=False,
        verbose_name="Use Global Default Image",
        help_text="Check this to ignore the custom image above and use the site-wide "
                  "default breadcrumb image instead."
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active",
        help_text="When checked, this page-level override is applied. "
                  "Uncheck to disable and fall back to the global default."
    )

    class Meta:
        verbose_name = "Page Breadcrumb Override"
        verbose_name_plural = "Page Breadcrumb Overrides"
        ordering = ['page_key']

    def __str__(self):
        return f"{self.get_page_key_display()} — {'Default' if self.use_default else 'Custom'}"

    def get_image(self):
        """Returns the resolved image URL for this page override."""
        if self.custom_image:
            return self.custom_image.url
        return self.custom_image_url or ''


class NSSPageSettings(models.Model):
    banner_title = models.CharField(max_length=200, default="National Service Scheme Chaitanya Science and Arts College, Pamgarh")
    banner_description = models.TextField(default="The NSS symbol is based on the 'Rath Wheel' of the Konark Sun Temple of Orissa. The giant wheel portrays the cycles of creation, preservation and release and signifies the movement in life across time and space. The design of the symbol, a simplified form of Sun Chariot Wheel primarily depicts movement. The wheel signifies the progressive cycle of life. It also stands for dynamism and progressive outlook of youth.")
    banner_image = models.ImageField(upload_to='nss/', blank=True, null=True)
    banner_image_url = models.URLField(blank=True, help_text="External URL for banner image if not uploaded locally")
    banner_icon = models.FileField(upload_to='nss/icons/', blank=True, null=True, help_text="SVG/PNG icon for banner")
    banner_icon_url = models.URLField(blank=True, help_text="External URL for banner icon if not uploaded locally")
    
    about_title = models.CharField(max_length=200, default="Our NSS Activities")
    about_description = models.TextField(default="The NSS Unit consists of 100 student volunteers. The Program Officer is expected to motivate the student youth to understand the values and philosophy of NSS. The overall functions of Program Officer are to help the students to plan, implement and evaluate the activities of NSS under his/her charge and give proper guidance and directions to the student volunteers.")

    class Meta:
        verbose_name = "NSS Page Settings"
        verbose_name_plural = "NSS Page Settings"

    def __str__(self):
        return "NSS Page Settings"

    def get_banner_image(self):
        if self.banner_image:
            return self.banner_image.url
        if not self.banner_image_url:
            return ""
        if self.banner_image_url.startswith(('http://', 'https://', '/')):
            return self.banner_image_url
        from django.conf import settings
        return f"{settings.MEDIA_URL}{self.banner_image_url}"

    def get_banner_icon(self):
        if self.banner_icon:
            return self.banner_icon.url
        if not self.banner_icon_url:
            return ""
        if self.banner_icon_url.startswith(('http://', 'https://', '/')):
            return self.banner_icon_url
        from django.conf import settings
        return f"{settings.MEDIA_URL}{self.banner_icon_url}"


class NSSActivity(models.Model):
    serial_number = models.CharField(max_length=10, help_text="e.g. 01, 02")
    title = models.CharField(max_length=300)
    fa_icon = models.CharField(max_length=100, default="fa-star", help_text="FontAwesome icon class name, e.g. 'fa-user-md', 'fa-tooth', 'fa-tree'")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'serial_number']
        verbose_name = "NSS Activity"
        verbose_name_plural = "NSS Activities"

    def __str__(self):
        return f"{self.serial_number} - {self.title}"


class NSSGalleryImage(models.Model):
    image = models.ImageField(upload_to='nss/gallery/', blank=True, null=True)
    image_url = models.URLField(blank=True, help_text="External URL for image if not uploaded locally")
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "NSS Gallery Image"
        verbose_name_plural = "NSS Gallery Images"

    def __str__(self):
        return self.caption or f"NSS Gallery Image {self.id}"

    def get_image(self):
        if self.image:
            return self.image.url
        if not self.image_url:
            return ""
        if self.image_url.startswith(('http://', 'https://', '/')):
            return self.image_url
        from django.conf import settings
        return f"{settings.MEDIA_URL}{self.image_url}"


class IICPageSettings(models.Model):
    title = models.CharField(max_length=200, default="INSTITUTION'S INNOVATION COUNCIL (IIC)")
    sub_title = models.CharField(max_length=200, default="Ministry of Education Supported")
    description = models.TextField(default="In the year 2018, the Ministry of Education (MoE) through MoE’s Innovation Cell (MIC) launched the Institution’s Innovation Council (IIC) program in collaboration with AICTE for Higher Educational Institutions (HEIs) to systematically foster the culture of innovation and start-up ecosystem in education institutions. Primarily, IIC’s role is to engage large number of faculty, students and staff in various innovation and entrepreneurship related activities such as ideation, Problem solving, Proof of Concept development, Design Thinking, IPR, project handling and management at Pre-incubation/Incubation stage, etc., so that innovation and entrepreneurship ecosystem gets established and stabilized in HEIs.")
    about_image_1 = models.ImageField(upload_to='iic/', blank=True, null=True)
    about_image_1_url = models.CharField(max_length=300, blank=True)
    about_image_2 = models.ImageField(upload_to='iic/', blank=True, null=True)
    about_image_2_url = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name = "IIC Page Settings"
        verbose_name_plural = "IIC Page Settings"

    def __str__(self):
        return self.title

    def get_about_image_1(self):
        if self.about_image_1:
            return self.about_image_1.url
        if not self.about_image_1_url:
            return ""
        if self.about_image_1_url.startswith(('http://', 'https://', '/')):
            return self.about_image_1_url
        from django.conf import settings
        return f"{settings.MEDIA_URL}{self.about_image_1_url}"

    def get_about_image_2(self):
        if self.about_image_2:
            return self.about_image_2.url
        if not self.about_image_2_url:
            return ""
        if self.about_image_2_url.startswith(('http://', 'https://', '/')):
            return self.about_image_2_url
        from django.conf import settings
        return f"{settings.MEDIA_URL}{self.about_image_2_url}"


class IICGalleryImage(models.Model):
    image = models.ImageField(upload_to='iic/gallery/', blank=True, null=True)
    image_url = models.URLField(blank=True, help_text="External URL for image if not uploaded locally")
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "IIC Gallery Image"
        verbose_name_plural = "IIC Gallery Images"

    def __str__(self):
        return self.caption or f"IIC Gallery Image {self.id}"

    def get_image(self):
        if self.image:
            return self.image.url
        if not self.image_url:
            return ""
        if self.image_url.startswith(('http://', 'https://', '/')):
            return self.image_url
        from django.conf import settings
        return f"{settings.MEDIA_URL}{self.image_url}"


class CampusMedia(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='video')
    title = models.CharField(max_length=200, help_text="e.g. Cleaner, Greener & Sustainable")
    image = models.ImageField(upload_to='campus_media/', blank=True, null=True, help_text="Upload cover image / photo")
    image_url = models.URLField(blank=True, help_text="External cover image URL if not uploading locally")
    video_url = models.URLField(blank=True, help_text="YouTube video URL (for Video type)")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Campus Media / Video"
        verbose_name_plural = "Campus Media & Videos"

    def __str__(self):
        return f"[{self.get_media_type_display()}] {self.title}"

    def get_image(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        if self.media_type == 'video' and self.video_url:
            video_id = self.get_youtube_video_id()
            if video_id:
                return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        from django.templatetags.static import static
        return static('assets/images/chaitanya_video.jpg')

    def get_youtube_video_id(self):
        if not self.video_url:
            return None
        import re
        regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
        match = re.search(regex, self.video_url)
        return match.group(1) if match else None



class Infrastructure(models.Model):
    title = models.CharField(max_length=200, help_text="e.g. Laboratories, Library, Seminar Hall")
    slug = models.SlugField(unique=True, max_length=200, blank=True, help_text="Auto-generated slug (leave blank to auto-generate)")
    description = models.TextField(help_text="Detailed description of the infrastructure")
    video_url = models.URLField(blank=True, help_text="Optional YouTube video URL for a tour/showcase of this infrastructure")
    order = models.PositiveIntegerField(default=0, help_text="Order in which it will be displayed")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Infrastructure Section"
        verbose_name_plural = "Infrastructure Sections"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('core:infrastructure_detail', args=[self.slug])

    def get_youtube_video_id(self):
        if not self.video_url:
            return None
        import re
        regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
        match = re.search(regex, self.video_url)
        return match.group(1) if match else None

    def get_video_embed_url(self):
        video_id = self.get_youtube_video_id()
        if video_id:
            return f"https://www.youtube-nocookie.com/embed/{video_id}"
        return None


class InfrastructureImage(models.Model):
    infrastructure = models.ForeignKey(Infrastructure, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='infrastructure/', blank=True, null=True, help_text="Upload local image")
    image_url = models.URLField(blank=True, help_text="Or enter external image URL")
    caption = models.CharField(max_length=250, blank=True, help_text="Subcategory or facility name shown on the detail page")
    description = models.TextField(
        blank=True,
        help_text="Optional description for this subcategory or image section on the detail page",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Infrastructure Image"
        verbose_name_plural = "Infrastructure Images"

    def __str__(self):
        return f"Image for {self.infrastructure.title} ({self.id})"

    def get_image(self):
        return self.image.url if self.image else self.image_url


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name="Category")
    name = models.CharField(max_length=200, verbose_name="Product Name")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    description = models.TextField(verbose_name="Description", help_text="Detailed product description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (INR)")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Product Image")
    image_url = models.URLField(blank=True, max_length=500, verbose_name="External Image URL", help_text="Fallback URL if no image is uploaded")
    in_stock = models.BooleanField(default=True, verbose_name="In Stock", help_text="Toggle stock availability status")
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    is_active = models.BooleanField(default=True, verbose_name="Is Active", help_text="Toggle visibility on the frontend")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url or "https://i.postimg.cc/k5Z5snNv/csac-naac.png"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Product")
    image = models.ImageField(upload_to='products/gallery/', blank=True, null=True, help_text="Upload gallery image")
    image_url = models.URLField(blank=True, max_length=500, verbose_name="External Image URL", help_text="Or external URL")
    caption = models.CharField(max_length=250, blank=True, help_text="Optional caption")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

    def __str__(self):
        return f"Image for {self.product.name} ({self.id})"

    def get_image(self):
        return self.image.url if self.image else self.image_url


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Product")
    reviewer_name = models.CharField(max_length=100, verbose_name="Your Name")
    reviewer_email = models.EmailField(verbose_name="Email Address")
    rating = models.PositiveIntegerField(default=5, verbose_name="Rating (1-5)")
    review_text = models.TextField(verbose_name="Review Content")
    is_approved = models.BooleanField(default=True, verbose_name="Approved", help_text="Toggle visibility on frontend")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Product Review"
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return f"Review ({self.rating}*) by {self.reviewer_name} for {self.product.name}"


class ProductInquiry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inquiries', verbose_name="Product")
    name = models.CharField(max_length=100, verbose_name="Full Name")
    email = models.EmailField(verbose_name="Email Address")
    phone = models.CharField(max_length=20, verbose_name="Phone Number")
    message = models.TextField(blank=True, verbose_name="Additional Message/Inquiry Details")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Product Inquiry"
        verbose_name_plural = "Product Inquiries"

    def __str__(self):
        return f"Inquiry from {self.name} for {self.product.name}"


class SportsPageSettings(models.Model):
    """Singleton model for Sports page content settings."""
    page_intro_title = models.CharField(max_length=200, default="Sports & Athletics at CSAC")
    page_intro = models.TextField(
        default="Chaitanya Science and Arts College believes in the all-round development of its students. Physical education and sports form an integral part of our curriculum. The college boasts excellent sports infrastructure, training programs and coaches that encourage students to participate at regional, state, and national levels.",
        help_text="Introduction paragraph shown at the top of the Sports page."
    )
    facilities = models.TextField(
        default="Outdoor Sports Ground (Cricket, Football, Athletics)\nIndoor Games Arena (Table Tennis, Chess, Carrom, Badminton)\nFitness Center & Gymnasium\nVolleyball & Basketball Courts\nSports Library & Media Room",
        help_text="List of sports facilities, one per line. Displayed as a bullet list."
    )
    achievements = models.TextField(
        default="Annual Athletic Meet — Inter-departmental athletics challenges\nChaitanya Trophy — Inter-collegiate Cricket & Volleyball tournament\nYoga Day Celebrations — Campus-wide training on International Yoga Day",
        help_text="Sports achievements/events, one per line."
    )
    policies = models.TextField(
        default="Sports quota admissions for outstanding regional/national players\nCash incentives and fee concessions for tournament winners\nSpecial academic support and attendance relief during tournaments",
        help_text="Sports policies/benefits, one per line."
    )
    show_notices = models.BooleanField(default=True, verbose_name="Show Sports Notices Section")
    show_events = models.BooleanField(default=True, verbose_name="Show Upcoming Sports Events Section")
    show_gallery = models.BooleanField(default=True, verbose_name="Show Sports Gallery Section")
    show_happenings = models.BooleanField(default=True, verbose_name="Show Sports Happenings Section")

    class Meta:
        verbose_name = "Sports Page Settings"
        verbose_name_plural = "Sports Page Settings"

    def __str__(self):
        return "Sports Page Settings"

    def get_facilities_list(self):
        return [line.strip() for line in self.facilities.splitlines() if line.strip()]

    def get_achievements_list(self):
        return [line.strip() for line in self.achievements.splitlines() if line.strip()]

    def get_policies_list(self):
        return [line.strip() for line in self.policies.splitlines() if line.strip()]


class TeachingStaffPageSettings(models.Model):
    """Singleton settings for the teaching staff listing page header."""
    title = models.CharField(
        max_length=200,
        default='Faculty List 2025-26',
        help_text='Main heading shown on the teaching staff page',
    )
    subtitle = models.TextField(
        default='Meet our dedicated, qualified, and experienced teaching staff members.',
        help_text='Short description shown below the heading',
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Teaching Staff Page Settings'
        verbose_name_plural = 'Teaching Staff Page Settings'

    def __str__(self):
        return self.title


class NonTeachingStaffPageSettings(models.Model):
    """Singleton settings for the non-teaching staff listing page header."""
    title = models.CharField(
        max_length=200,
        default='Non-Teaching Staff',
        help_text='Main heading shown on the non-teaching staff page',
    )
    subtitle = models.TextField(
        default='Meet our dedicated administrative and support staff members.',
        help_text='Short description shown below the heading',
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Non-Teaching Staff Page Settings'
        verbose_name_plural = 'Non-Teaching Staff Page Settings'

    def __str__(self):
        return self.title


class NonTeachingStaffMember(models.Model):
    name = models.CharField(max_length=150)
    designation = models.CharField(max_length=200)
    department_section = models.CharField(
        max_length=200,
        verbose_name='Department / Section',
        help_text='e.g. Administration, Accounts, Library',
    )
    qualification = models.CharField(max_length=300, blank=True)
    contact = models.CharField(
        max_length=100,
        blank=True,
        help_text='Phone number or email',
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Non-Teaching Staff Member'
        verbose_name_plural = 'Non-Teaching Staff Members'

    def __str__(self):
        return f"{self.name} ({self.designation})"


class SportsGalleryImage(models.Model):
    image = models.ImageField(upload_to='sports/gallery/', blank=True, null=True)
    image_url = models.URLField(blank=True, max_length=500, help_text="External URL for image if not uploaded locally")
    caption = models.CharField(max_length=200, blank=True)
    sport_tag = models.CharField(max_length=100, blank=True, help_text="e.g. Cricket, Volleyball, Athletics")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Sports Gallery Image"
        verbose_name_plural = "Sports Gallery Images"

    def __str__(self):
        return self.caption or f"Sports Gallery Image {self.id}"

    def get_image(self):
        if self.image:
            return self.image.url
        if not self.image_url:
            return ""
        return self.image_url


class NEPTab(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tab Title", help_text="e.g. NEP Syllabus, General Guidelines")
    description = CKEditor5Field('Description', config_name='extends', blank=True, help_text="The main rich text content displayed inside this tab.")
    order = models.PositiveIntegerField(default=0, help_text="For ordering tabs on the page.")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "NEP Tab"
        verbose_name_plural = "NEP Tabs"

    def __str__(self):
        return self.title


class NEPTabFile(models.Model):
    tab = models.ForeignKey(NEPTab, on_delete=models.CASCADE, related_name='files', verbose_name="NEP Tab")
    file = models.FileField(upload_to='nep/files/', verbose_name="Upload File")
    title = models.CharField(max_length=250, verbose_name="File Title/Label", help_text="e.g. NEP Syllabus PDF, Academic Credit Rules")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "NEP Tab File"
        verbose_name_plural = "NEP Tab Files"

    def __str__(self):
        return f"{self.title} (under {self.tab.title})"


class NEPTabLink(models.Model):
    tab = models.ForeignKey(NEPTab, on_delete=models.CASCADE, related_name='links', verbose_name="NEP Tab")
    url = models.URLField(max_length=500, verbose_name="Web Link / URL")
    title = models.CharField(max_length=250, verbose_name="Link Label/Text", help_text="e.g. Official ABC Portal, Digilocker Website")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "NEP Tab Link"
        verbose_name_plural = "NEP Tab Links"

    def __str__(self):
        return f"{self.title} (under {self.tab.title})"


class LibraryPageSettings(models.Model):
    page_intro_title = models.CharField(max_length=200, default="Learning Resources of the College: Smt. Urmila Devi Smriti Pustkaalaya")
    page_intro = models.TextField(
        default="Discover the heart of academic exploration at the College Library, established in 2001 in loving memory of Smt. Urmila Devi. More than just a repository of knowledge, our library is a dynamic hub that caters to the diverse needs of both faculty and students."
    )
    about_library_title = models.CharField(max_length=200, default="About The Library")
    about_library_text = models.TextField(
        default="With a spacious environment welcoming up to 100 readers, we offer semi-automated services and house an impressive collection of 2000 physical books and research journals. Access to digital subscriptions such as INFIBNET and open-access journals enriches research opportunities. With RFID technology ensuring seamless operations, our library hosts a variety of engaging activities, including orientation programs, faculty development seminars, and participatory reading club activities. Guided by our dedicated Library Committee, we are committed to fostering a culture of learning and intellectual exploration. Welcome to your gateway to knowledge and inspiration."
    )
    future_plan_title = models.CharField(max_length=200, default="Future Plan")
    future_plan_text = models.TextField(
        default="The future plan for the library involves expanding its physical space and digital infrastructure to accommodate growth and enhance accessibility. This includes fully automating processes like book checkouts and inventory management, while also prioritizing the digitization of collections and integration of digital resources. Collaborative partnerships, user training, and ongoing evaluation will ensure that the library remains a cutting-edge hub for research and learning in the digital age."
    )
    library_image = models.ImageField(upload_to='library/', blank=True, null=True)
    library_image_url = models.CharField(max_length=500, blank=True, default="/static/assets/images/feature/0001.png")
    sections_text = models.TextField(
        default="Reference Section\nCirculation Section\nPeriodical Section",
        help_text="Enter one section per line."
    )
    about_services_text = models.TextField(
        default="The library has automated all its library activities to provide effective and wide range of academic resources such as books, journals, online databases."
    )
    new_suggestion_text = models.TextField(
        default="The library always encourages all students and faculty to recommend new books in order to strengthen their collection."
    )

    class Meta:
        verbose_name = "Library Page Settings"
        verbose_name_plural = "Library Page Settings"

    def __str__(self):
        return "Library Page Settings"

    def get_sections_list(self):
        return [line.strip() for line in self.sections_text.splitlines() if line.strip()]

    def get_image(self):
        if self.library_image:
            return self.library_image.url
        return self.library_image_url or "/static/assets/images/feature/0001.png"


class LibraryBookCategory(models.Model):
    category_name = models.CharField(max_length=200, verbose_name="Category")
    num_books = models.PositiveIntegerField(verbose_name="No. of Books")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Library Book Category"
        verbose_name_plural = "Library Book Categories"

    def __str__(self):
        return f"{self.category_name} ({self.num_books} books)"


class LibraryResource(models.Model):
    name = models.CharField(max_length=200, verbose_name="Name")
    website_url = models.URLField(max_length=500, verbose_name="Website")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Library Resource"
        verbose_name_plural = "Library Resources"

    def __str__(self):
        return self.name


class LibraryBookSuggestion(models.Model):
    book_title = models.CharField(max_length=200, verbose_name="Book Title")
    author = models.CharField(max_length=200, verbose_name="Author")
    recommended_by = models.CharField(max_length=150, verbose_name="Recommended By")
    email = models.EmailField(verbose_name="Email Address")
    reason = models.TextField(blank=True, verbose_name="Reason for Suggestion")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Library Book Suggestion"
        verbose_name_plural = "Library Book Suggestions"

    def __str__(self):
        return f"Suggestion: {self.book_title} by {self.recommended_by}"


class LibraryGalleryImage(models.Model):
    settings = models.ForeignKey(LibraryPageSettings, on_delete=models.CASCADE, related_name='images', verbose_name="Library Settings")
    image = models.ImageField(upload_to='library/gallery/', blank=True, null=True, help_text="Upload local image")
    image_url = models.URLField(blank=True, max_length=500, help_text="Or enter external image URL")
    caption = models.CharField(max_length=250, blank=True, help_text="Optional caption for the image")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Library Gallery Image"
        verbose_name_plural = "Library Gallery Images"

    def __str__(self):
        return self.caption or f"Library Image {self.id} for settings {self.settings.id}"

    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url or ""


class MenuItem(models.Model):
    title = models.CharField(max_length=100, help_text="Display name for the menu item")
    url = models.CharField(
        max_length=255, 
        help_text="URL path (e.g. /about/) or named Django URL pattern (e.g. core:about) or external link (e.g. https://...)"
    )
    is_named_url = models.BooleanField(
        default=False, 
        verbose_name="Is Named URL",
        help_text="Check if the URL is a Django URL name pattern (e.g. 'core:about')"
    )
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children',
        help_text="Select parent menu item. Leave blank to make it a top-level menu."
    )
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers come first)")
    is_active = models.BooleanField(default=True, help_text="Toggle visibility on the navbar")
    open_in_new_tab = models.BooleanField(default=False, verbose_name="Open in new tab")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"

    def __str__(self):
        if self.parent:
            return f"{self.parent.title} > {self.title}"
        return self.title

    def get_absolute_url(self):
        if self.is_named_url:
            from django.urls import reverse, NoReverseMatch
            try:
                # Handle URLs with arguments if they are split by spaces, e.g. "academics:department_detail 'hindi'"
                parts = self.url.split()
                url_name = parts[0]
                url_args = [arg.strip("'\"") for arg in parts[1:]]
                return reverse(url_name, args=url_args)
            except NoReverseMatch:
                return self.url
        return self.url


class VisitorCount(models.Model):
    count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Visitor Count"
        verbose_name_plural = "Visitor Count"

    def __str__(self):
        return f"Total Visitors: {self.count}"


class UploadedDocument(models.Model):
    title = models.CharField(max_length=200, help_text="Enter a name/title for the document")
    file = models.FileField(upload_to='documents/', help_text="Choose the PDF, Doc, or Image file")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Uploaded Document"
        verbose_name_plural = "Uploaded Documents"

    def __str__(self):
        return self.title


