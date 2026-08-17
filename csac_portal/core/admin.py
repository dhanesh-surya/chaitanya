from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SiteSettings, BannerSlide, AccreditationLogo,
    StatCounter, CollegeInfo, Leadership, Committee, CommitteeMember,
    Policy, Achievement, Notice, ImportantLink, CareerGuidanceSubmission,
    SocialScheme, Testimonial, Event, Happening, HappeningImage, QuickLinkCard,
    AboutPage, Recognition, CommitteeActivity, CommitteeGalleryImage,
    UGCTable, UGCDocument, UGCPageSettings, UGCGrant, PopupAnnouncement,
    BreadcrumbSettings, PageBreadcrumb, NSSPageSettings, NSSActivity, NSSGalleryImage,
    IICPageSettings, IICGalleryImage, CampusMedia, Infrastructure, InfrastructureImage,
    Product, ProductInquiry, ProductCategory, ProductImage, ProductReview,
    SportsPageSettings, SportsGalleryImage, TeachingStaffPageSettings, NonTeachingStaffPageSettings,
    NonTeachingStaffMember,
    NEPTab, NEPTabFile, NEPTabLink,
    LibraryPageSettings, LibraryBookCategory, LibraryResource, LibraryBookSuggestion, LibraryGalleryImage,
    MenuItem
)
from .forms import (
    SiteSettingsForm, CommitteeForm, CommitteeMemberForm,
    CommitteeActivityForm, CommitteeGalleryImageForm,
    PolicyForm, NoticeForm, EventForm, UGCTableForm, UGCDocumentForm,
    UGCPageSettingsForm, UGCGrantForm, BreadcrumbSettingsForm, PageBreadcrumbForm,
    NSSPageSettingsForm, NSSActivityForm, NSSGalleryImageForm,
    IICPageSettingsForm, IICGalleryImageForm, CampusMediaForm, TestimonialForm,
    InfrastructureForm, InfrastructureImageForm, AccreditationLogoForm, QuickLinkCardForm,
    ProductForm, ProductInquiryForm, ProductReviewForm,
    SportsPageSettingsForm, SportsGalleryImageForm, TeachingStaffPageSettingsForm, NonTeachingStaffPageSettingsForm,
    NonTeachingStaffMemberForm,
    NEPTabForm, NEPTabFileForm, NEPTabLinkForm,
    LibraryPageSettingsForm, LibraryBookCategoryForm, LibraryResourceForm, LibraryBookSuggestionForm,
    LibraryGalleryImageForm, MenuItemForm
)



@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    form = SiteSettingsForm
    list_display = ('college_name_en', 'phone', 'email')
    fieldsets = (
        ('College Name (English) Settings', {
            'fields': (
                'college_name_en',
                ('college_name_en_font_family', 'college_name_en_google_font_url'),
                ('college_name_en_font_size', 'college_name_en_font_color')
            )
        }),
        ('College Name (Hindi) Settings', {
            'fields': (
                'college_name_hi',
                ('college_name_hi_font_family', 'college_name_hi_google_font_url'),
                ('college_name_hi_font_size', 'college_name_hi_font_color')
            )
        }),
        ('Tagline Settings', {
            'fields': (
                'tagline',
                ('tagline_font_family', 'tagline_google_font_url'),
                ('tagline_font_size', 'tagline_font_color')
            )
        }),
        ('Branding & Logos', {'fields': ('college_logo', 'college_logo_mobile', 'logo2', 'logo3', 'logo4', 'logo5')}),
        ('Header Layout Settings', {
            'fields': (
                'use_image_header',
                'header_image',
            )
        }),
        ('Contact Settings', {
            'fields': (
                'address_line1',
                ('address_line1_font_family', 'address_line1_google_font_url'),
                ('address_line1_font_size', 'address_line1_font_color'),
                'address_line2',
                ('address_line2_font_family', 'address_line2_google_font_url'),
                ('address_line2_font_size', 'address_line2_font_color'),
                ('phone', 'email')
            )
        }),
        ('Social Media', {'fields': ('facebook_url', 'youtube_url', 'instagram_url')}),
        ('Map', {'fields': ('google_maps_embed',)}),
        ('Other', {'fields': ('established_year',)}),
    )



@admin.register(BannerSlide)
class BannerSlideAdmin(admin.ModelAdmin):
    list_display = ('caption', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('caption',)


@admin.register(AccreditationLogo)
class AccreditationLogoAdmin(admin.ModelAdmin):
    form = AccreditationLogoForm
    list_display = ('image_preview', 'name', 'order', 'link')
    list_editable = ('order',)
    search_fields = ('name',)

    def image_preview(self, obj):
        url = obj.get_image()
        if url:
            return format_html('<img src="{}" style="height:50px;border-radius:4px;object-fit:cover;" />', url)
        return '—'
    image_preview.short_description = 'Preview'


@admin.register(StatCounter)
class StatCounterAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'order')
    list_editable = ('value', 'order')


@admin.register(CollegeInfo)
class CollegeInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'order')
    list_filter = ('section',)
    list_editable = ('order',)


@admin.register(Leadership)
class LeadershipAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'email', 'order')
    list_filter = ('role',)
    list_editable = ('order',)
    search_fields = ('name', 'email', 'qualification')


class CommitteeMemberInline(admin.TabularInline):
    model = CommitteeMember
    form = CommitteeMemberForm
    extra = 1
    fields = ('name', 'designation', 'role_in_committee', 'order')


class CommitteeActivityInline(admin.TabularInline):
    model = CommitteeActivity
    form = CommitteeActivityForm
    extra = 1
    fields = ('title', 'description', 'date', 'image', 'order')


class CommitteeGalleryImageInline(admin.TabularInline):
    model = CommitteeGalleryImage
    form = CommitteeGalleryImageForm
    extra = 1
    fields = ('image', 'caption', 'order')


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    form = CommitteeForm
    list_display = ('name', 'slug', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [CommitteeMemberInline, CommitteeActivityInline, CommitteeGalleryImageInline]


@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    form = PolicyForm
    list_display = ('title', 'order')
    list_editable = ('order',)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'order')
    list_filter = ('year',)
    list_editable = ('order',)


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    form = NoticeForm
    list_display = ('title', 'category', 'published_date', 'show_in_marquee', 'is_active')
    list_filter = ('category', 'is_active', 'show_in_marquee', 'published_date')
    list_editable = ('category', 'show_in_marquee', 'is_active')
    search_fields = ('title',)


@admin.register(ImportantLink)
class ImportantLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'category', 'order')
    list_filter = ('category',)
    list_editable = ('order',)


@admin.register(CareerGuidanceSubmission)
class CareerGuidanceSubmissionAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname', 'email', 'phone', 'submitted_at')
    readonly_fields = ('fname', 'lname', 'email', 'phone', 'msg', 'submitted_at')
    search_fields = ('fname', 'lname', 'email', 'phone', 'msg')
    list_filter = ('submitted_at',)

    def has_add_permission(self, request):
        return False


@admin.register(SocialScheme)
class SocialSchemeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'category')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    form = TestimonialForm
    list_display = ('photo_preview', 'student_name', 'program', 'rating', 'order')
    list_editable = ('rating', 'order')
    search_fields = ('student_name', 'program', 'text')

    def photo_preview(self, obj):
        url = obj.get_photo()
        if url:
            return format_html('<img src="{}" style="height:50px;width:50px;border-radius:50%;object-fit:cover;" />', url)
        return "-"
    photo_preview.short_description = 'Photo'

    fieldsets = (
        ('Student Information', {
            'fields': ('student_name', 'program', 'rating', 'order')
        }),
        ('Testimonial Content', {
            'fields': ('text',)
        }),
        ('Media/Photo', {
            'fields': ('photo', 'photo_url')
        }),
    )



@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventForm
    list_display = ('title', 'date', 'time', 'location', 'is_active', 'is_sports_event')
    list_editable = ('is_active', 'is_sports_event')
    search_fields = ('title', 'location')
    list_filter = ('date', 'is_active', 'is_sports_event')
    fieldsets = (
        ('General Information', {
            'fields': ('title', 'date', 'time', 'location', 'is_active', 'is_sports_event')
        }),
        ('Event Details', {
            'fields': ('description',)
        }),
        ('Attachments & Media', {
            'fields': ('image', 'image_url', 'brochure', 'youtube_url')
        }),
        ('Registration & Actions', {
            'fields': ('registration_link', 'link')
        }),
    )


class HappeningImageInline(admin.TabularInline):
    model = HappeningImage
    extra = 3
    fields = ('image', 'image_url', 'caption', 'order')


@admin.register(Happening)
class HappeningAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'department', 'date', 'order', 'is_sports_activity')
    list_editable = ('order', 'is_sports_activity')
    search_fields = ('title', 'category')
    list_filter = ('date', 'category', 'department', 'is_sports_activity')
    inlines = [HappeningImageInline]


@admin.register(QuickLinkCard)
class QuickLinkCardAdmin(admin.ModelAdmin):
    form = QuickLinkCardForm
    list_display = ('title', 'link', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'link')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'link', 'fa_icon', 'icon', 'icon_url', 'order', 'is_active')
        }),
        ('Card Design / Customization', {
            'fields': ('bg_color', 'bg_image', 'overlay_color', 'overlay_opacity'),
            'description': 'Customize the card background color or background image, and configure a semi-transparent color overlay.'
        }),
    )


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('page_title', 'about_us_title')
    
    fieldsets = (
        ('General & Header Settings', {
            'fields': ('page_title', 'breadcrumb_image', 'breadcrumb_image_url')
        }),
        ('About Us Main Section', {
            'fields': ('about_us_title', 'about_us_description_1', 'about_us_description_2', 'about_us_description_3', 'about_us_image', 'about_us_image_url')
        }),
        ('Counter Stats (Next to Image)', {
            'fields': (
                ('stat1_value', 'stat1_label', 'stat1_icon'),
                ('stat2_value', 'stat2_label', 'stat2_icon'),
                ('stat3_value', 'stat3_label', 'stat3_icon'),
            )
        }),
        ('Fun Facts (Red Banner Bar)', {
            'fields': (
                ('funfact1_value', 'funfact1_label'),
                ('funfact2_value', 'funfact2_label'),
                ('funfact3_value', 'funfact3_label'),
            )
        }),
        ('Vision & Mission', {
            'fields': ('mission_statement', 'vision_title', 'vision_text', 'mission_title', 'mission_text_1', 'mission_text_2')
        }),
        ('Governance', {
            'fields': ('governance_title', 'governance_text')
        }),
        ('Distinctive Features', {
            'fields': ('features_title', 'features_list')
        }),
        ('Principal Testimonial', {
            'fields': ('testimonial_text', 'testimonial_author', 'testimonial_author_image')
        }),
    )


@admin.register(Recognition)
class RecognitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    search_fields = ('title',)


class UGCDocumentInline(admin.TabularInline):
    model = UGCDocument
    form = UGCDocumentForm
    extra = 3
    fields = ('sn', 'title', 'file', 'file_url')


@admin.register(UGCTable)
class UGCTableAdmin(admin.ModelAdmin):
    form = UGCTableForm
    list_display = ('name', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('name',)
    inlines = [UGCDocumentInline]


@admin.register(UGCDocument)
class UGCDocumentAdmin(admin.ModelAdmin):
    form = UGCDocumentForm
    list_display = ('title', 'ugc_table', 'sn')
    list_filter = ('ugc_table',)
    search_fields = ('title',)


@admin.register(UGCPageSettings)
class UGCPageSettingsAdmin(admin.ModelAdmin):
    form = UGCPageSettingsForm
    list_display = ('heading', 'show_ugc_details', 'show_grants_section')
    
    fieldsets = (
        ('Header & Introduction', {
            'fields': ('heading', 'description')
        }),
        ('UGC Details Cards', {
            'fields': ('show_ugc_details', 'autonomy_status_title', 'autonomy_status_subtitle', 'autonomy_status_text', 'status_2f_12b_title', 'status_2f_12b_text', 'benefits_title', 'benefits_list')
        }),
        ('Grants Section Settings', {
            'fields': ('show_grants_section', 'grants_title')
        }),
    )

    def has_add_permission(self, request):
        if UGCPageSettings.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(UGCGrant)
class UGCGrantAdmin(admin.ModelAdmin):
    form = UGCGrantForm
    list_display = ('scheme', 'purpose', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('scheme', 'purpose')


@admin.register(PopupAnnouncement)
class PopupAnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order', 'show_once_per_session', 'updated_at')
    list_editable = ('is_active', 'order', 'show_once_per_session')
    list_filter = ('is_active', 'show_once_per_session')
    search_fields = ('title', 'text')
    fieldsets = (
        ('General Details', {
            'fields': ('title', 'is_active', 'order', 'show_once_per_session')
        }),
        ('Announcement Content', {
            'fields': ('image', 'image_url', 'text')
        }),
        ('Action / Call-to-Action Link', {
            'fields': ('link', 'link_text')
        }),
    )


@admin.register(BreadcrumbSettings)
class BreadcrumbSettingsAdmin(admin.ModelAdmin):
    form = BreadcrumbSettingsForm
    list_display = ('__str__', 'is_active', 'image_preview')

    fieldsets = (
        ('Global Default Image', {
            'description': 'Upload or link a default breadcrumb background image used across all pages. '
                           'Per-page overrides can be set in "Page Breadcrumb Overrides" below.',
            'fields': ('default_image', 'default_image_url'),
        }),
        ('Per-Page Override Switch', {
            'fields': ('is_active',),
            'description': 'When checked, individual pages can have their own breadcrumb images '
                           '(set in "Page Breadcrumb Overrides"). When unchecked, all pages use '
                           'only the global default image above.',
        }),
    )

    def image_preview(self, obj):
        url = obj.get_image()
        if url:
            return format_html('<img src="{}" style="height:50px;border-radius:4px;object-fit:cover;" />', url)
        return '—'
    image_preview.short_description = 'Preview'

    def has_add_permission(self, request):
        # Singleton: prevent creating more than one row
        if BreadcrumbSettings.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PageBreadcrumb)
class PageBreadcrumbAdmin(admin.ModelAdmin):
    form = PageBreadcrumbForm
    list_display = ('get_page_key_display', 'is_active', 'use_default', 'image_preview')
    list_editable = ('is_active', 'use_default')
    list_filter = ('is_active', 'use_default')
    search_fields = ('page_key',)

    fieldsets = (
        ('Page Target', {
            'fields': ('page_key',),
            'description': 'Select which page this breadcrumb image override applies to.',
        }),
        ('Custom Image', {
            'fields': ('custom_image', 'custom_image_url'),
            'description': 'Upload a local image or provide an external URL. '
                           'Leave blank and check "Use Global Default" to inherit the site-wide default.',
        }),
        ('Behaviour Controls', {
            'fields': ('use_default', 'is_active'),
            'description': '"Use Global Default" overrides any custom image above and uses the global default instead. '
                           '"Active" toggles whether this entry is applied at all.',
        }),
    )

    def image_preview(self, obj):
        url = obj.get_image()
        if url:
            return format_html('<img src="{}" style="height:50px;border-radius:4px;object-fit:cover;" />', url)
        label = 'Default' if obj.use_default else '—'
        return label
    image_preview.short_description = 'Preview'

    def get_page_key_display(self, obj):
        return obj.get_page_key_display()
    get_page_key_display.short_description = 'Page'


@admin.register(NSSPageSettings)
class NSSPageSettingsAdmin(admin.ModelAdmin):
    form = NSSPageSettingsForm
    list_display = ('banner_title', 'about_title')
    
    def has_add_permission(self, request):
        if NSSPageSettings.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(NSSActivity)
class NSSActivityAdmin(admin.ModelAdmin):
    form = NSSActivityForm
    list_display = ('serial_number', 'title', 'fa_icon', 'order')
    list_editable = ('fa_icon', 'order')
    search_fields = ('title', 'serial_number')


@admin.register(NSSGalleryImage)
class NSSGalleryImageAdmin(admin.ModelAdmin):
    form = NSSGalleryImageForm
    list_display = ('__str__', 'order', 'image_preview')
    list_editable = ('order',)

    def image_preview(self, obj):
        url = obj.get_image()
        if url:
            return format_html('<img src="{}" style="height:50px;border-radius:4px;object-fit:cover;" />', url)
        return '—'
    image_preview.short_description = 'Preview'


@admin.register(IICPageSettings)
class IICPageSettingsAdmin(admin.ModelAdmin):
    form = IICPageSettingsForm
    list_display = ('title', 'sub_title')

    def has_add_permission(self, request):
        if IICPageSettings.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(IICGalleryImage)
class IICGalleryImageAdmin(admin.ModelAdmin):
    form = IICGalleryImageForm
    list_display = ('__str__', 'order', 'image_preview')
    list_editable = ('order',)

    def image_preview(self, obj):
        url = obj.get_image()
        if url:
            return format_html('<img src="{}" style="height:50px;border-radius:4px;object-fit:cover;" />', url)
        return '—'
    image_preview.short_description = 'Preview'


@admin.register(CampusMedia)
class CampusMediaAdmin(admin.ModelAdmin):
    form = CampusMediaForm
    list_display = ('title', 'media_type', 'order', 'is_active', 'image_preview')
    list_editable = ('order', 'is_active')
    list_filter = ('media_type', 'is_active')
    search_fields = ('title', 'video_url')

    def image_preview(self, obj):
        url = obj.get_image()
        if url:
            return format_html('<img src="{}" style="height:50px;border-radius:4px;object-fit:cover;" />', url)
        return '—'
    image_preview.short_description = 'Preview'

class InfrastructureImageInline(admin.TabularInline):
    model = InfrastructureImage
    form = InfrastructureImageForm
    extra = 1
    fields = ('image', 'image_url', 'caption', 'description', 'order')


@admin.register(Infrastructure)
class InfrastructureAdmin(admin.ModelAdmin):
    form = InfrastructureForm
    list_display = ('title', 'slug', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [InfrastructureImageInline]


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2
    fields = ('image', 'image_url', 'caption', 'order')


class ProductReviewInline(admin.TabularInline):
    model = ProductReview
    form = ProductReviewForm
    extra = 1
    fields = ('reviewer_name', 'reviewer_email', 'rating', 'review_text', 'is_approved')


class ProductInquiryInline(admin.TabularInline):
    model = ProductInquiry
    readonly_fields = ('name', 'email', 'phone', 'message', 'created_at')
    extra = 0
    can_delete = True

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('image_preview', 'name', 'category', 'price', 'in_stock', 'is_active', 'order')
    list_editable = ('category', 'price', 'in_stock', 'is_active', 'order')
    search_fields = ('name', 'description')
    list_filter = ('category', 'in_stock', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductReviewInline, ProductInquiryInline]

    def image_preview(self, obj):
        url = obj.get_image()
        if url:
            return format_html('<img src="{}" style="height:50px;border-radius:4px;object-fit:cover;" />', url)
        return '—'
    image_preview.short_description = 'Preview'


@admin.register(ProductInquiry)
class ProductInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'product', 'created_at')
    list_filter = ('product', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    readonly_fields = ('product', 'name', 'email', 'phone', 'message', 'created_at')

    def has_add_permission(self, request):
        return False


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer_name', 'reviewer_email', 'product', 'rating', 'is_approved', 'created_at')
    list_editable = ('is_approved',)
    list_filter = ('product', 'rating', 'is_approved', 'created_at')
    search_fields = ('reviewer_name', 'reviewer_email', 'review_text')


@admin.register(TeachingStaffPageSettings)
class TeachingStaffPageSettingsAdmin(admin.ModelAdmin):
    form = TeachingStaffPageSettingsForm
    list_display = ('title',)

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return True


@admin.register(NonTeachingStaffPageSettings)
class NonTeachingStaffPageSettingsAdmin(admin.ModelAdmin):
    form = NonTeachingStaffPageSettingsForm
    list_display = ('title',)

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return True


@admin.register(NonTeachingStaffMember)
class NonTeachingStaffMemberAdmin(admin.ModelAdmin):
    form = NonTeachingStaffMemberForm
    list_display = ('name', 'designation', 'department_section', 'order', 'is_active')
    list_filter = ('department_section', 'is_active')
    search_fields = ('name', 'designation', 'department_section', 'contact')
    list_editable = ('order', 'is_active')


@admin.register(SportsPageSettings)
class SportsPageSettingsAdmin(admin.ModelAdmin):
    form = SportsPageSettingsForm
    list_display = ('page_intro_title', 'show_notices', 'show_events', 'show_gallery', 'show_happenings')
    fieldsets = (
        ('Page Introduction', {
            'fields': ('page_intro_title', 'page_intro')
        }),
        ('Facilities & Achievements', {
            'fields': ('facilities', 'achievements', 'policies'),
            'description': 'Enter each item on a new line. They will be rendered as bullet lists on the sports page.'
        }),
        ('Section Visibility Controls', {
            'fields': ('show_notices', 'show_events', 'show_gallery', 'show_happenings'),
        }),
    )

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return True


@admin.register(SportsGalleryImage)
class SportsGalleryImageAdmin(admin.ModelAdmin):
    form = SportsGalleryImageForm
    list_display = ('image_preview', 'caption', 'sport_tag', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('caption', 'sport_tag')
    list_filter = ('sport_tag', 'is_active')

    def image_preview(self, obj):
        url = obj.get_image()
        if url:
            return format_html('<img src="{}" style="height:50px;border-radius:4px;object-fit:cover;" />', url)
        return '—'
    image_preview.short_description = 'Preview'


class NEPTabFileInline(admin.TabularInline):
    model = NEPTabFile
    form = NEPTabFileForm
    extra = 1


class NEPTabLinkInline(admin.TabularInline):
    model = NEPTabLink
    form = NEPTabLinkForm
    extra = 1


@admin.register(NEPTab)
class NEPTabAdmin(admin.ModelAdmin):
    form = NEPTabForm
    list_display = ('title', 'order', 'is_active', 'updated_at')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')
    list_filter = ('is_active',)
    inlines = [NEPTabFileInline, NEPTabLinkInline]


class LibraryGalleryImageInline(admin.TabularInline):
    model = LibraryGalleryImage
    form = LibraryGalleryImageForm
    extra = 2


@admin.register(LibraryPageSettings)
class LibraryPageSettingsAdmin(admin.ModelAdmin):
    form = LibraryPageSettingsForm
    list_display = ('page_intro_title', 'about_library_title', 'future_plan_title')
    inlines = [LibraryGalleryImageInline]
    fieldsets = (
        ('Page Banner & Introduction', {
            'fields': ('page_intro_title', 'page_intro', 'library_image', 'library_image_url')
        }),
        ('About Library & Future Plan', {
            'fields': ('about_library_title', 'about_library_text', 'future_plan_title', 'future_plan_text')
        }),
        ('Library Services & Suggestions', {
            'fields': ('sections_text', 'about_services_text', 'new_suggestion_text')
        }),
    )

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return True


@admin.register(LibraryBookCategory)
class LibraryBookCategoryAdmin(admin.ModelAdmin):
    form = LibraryBookCategoryForm
    list_display = ('category_name', 'num_books', 'order')
    list_editable = ('num_books', 'order')
    search_fields = ('category_name',)


@admin.register(LibraryResource)
class LibraryResourceAdmin(admin.ModelAdmin):
    form = LibraryResourceForm
    list_display = ('name', 'website_url', 'order')
    list_editable = ('website_url', 'order')
    search_fields = ('name',)


@admin.register(LibraryBookSuggestion)
class LibraryBookSuggestionAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'author', 'recommended_by', 'email', 'created_at')
    readonly_fields = ('book_title', 'author', 'recommended_by', 'email', 'reason', 'created_at')
    search_fields = ('book_title', 'author', 'recommended_by', 'email', 'reason')
    list_filter = ('created_at',)

    def has_add_permission(self, request):
        return False


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    form = MenuItemForm
    list_display = ('title', 'url', 'parent', 'order', 'is_active', 'open_in_new_tab')
    list_filter = ('is_active', 'open_in_new_tab', 'parent')
    list_editable = ('order', 'is_active', 'open_in_new_tab')
    search_fields = ('title', 'url')


from .models import VisitorCount

@admin.register(VisitorCount)
class VisitorCountAdmin(admin.ModelAdmin):
    list_display = ('count',)


from .models import UploadedDocument

@admin.register(UploadedDocument)
class UploadedDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'get_file_link')
    readonly_fields = ('direct_link',)

    def get_file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">View File</a>', obj.file.url)
        return "-"
    get_file_link.short_description = "Link"

    def direct_link(self, obj):
        if obj.file:
            return format_html(
                '<input type="text" value="{}" readonly style="width: 70%; padding: 6px; font-family: monospace;" onclick="this.select(); document.execCommand(\'copy\'); alert(\'Copied to clipboard!\');"> <small style="color: #666;">(Click to select/copy)</small>',
                obj.file.url
            )
        return "Save the document first to generate a link."
    direct_link.short_description = "Direct File URL"


