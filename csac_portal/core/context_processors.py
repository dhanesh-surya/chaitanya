from .models import SiteSettings, ImportantLink, Notice
from .models import BreadcrumbSettings, PageBreadcrumb


def site_context(request):
    """Makes site-wide data available in every template"""
    try:
        settings_obj = SiteSettings.objects.first()
    except Exception:
        settings_obj = None

    # Retrieve uploaded notices set to show in marquee
    n_list = Notice.objects.filter(show_in_marquee=True, is_active=True).order_by('-published_date')

    # Build marquee notices list
    combined_marquee = []
    for n in n_list:
        link = n.document.url if n.document else n.document_url
        combined_marquee.append({
            'text': n.title,
            'link': link,
            'flag': n.marquee_flag,
        })

    important_links = ImportantLink.objects.filter(category='important')
    quick_links = ImportantLink.objects.filter(category='quick')

    # ------------------------------------------------------------------
    # Breadcrumb image resolver
    # Pre-resolves all page keys into a dict so templates can use
    # dot-notation:  breadcrumb_images.about  (no function call needed)
    # ------------------------------------------------------------------
    try:
        _bc_global = BreadcrumbSettings.objects.first()
    except Exception:
        _bc_global = None

    try:
        _bc_pages = {pb.page_key: pb for pb in PageBreadcrumb.objects.all()}
    except Exception:
        _bc_pages = {}

    def _resolve(page_key):
        """
        Resolves the breadcrumb image for a given page key.

        - The global default image ALWAYS applies if uploaded (regardless of is_active).
        - is_active controls whether per-page overrides can replace the global.
        - Per-page override with use_default=True → global image.
        - Per-page override with custom image → that image (only when is_active=True).
        """
        global_img = _bc_global.get_image() if _bc_global else ''

        # If per-page overrides are enabled, check for one
        if _bc_global and _bc_global.is_active:
            page_override = _bc_pages.get(page_key)
            if page_override and page_override.is_active:
                if page_override.use_default:
                    return global_img
                img = page_override.get_image()
                if img:
                    return img

        # Always fall back to the global image
        return global_img

    # Build a flat dict for every known page key
    _all_keys = [
        'about', 'committees', 'committee_detail', 'policies', 'recognition',
        'staff_teaching', 'staff_nonteaching', 'notices', 'contact', 'nss',
        'iic', 'ugc', 'nep', 'sports', 'co_po', 'happenings',
        'happening_detail', 'event_detail',
        'academics_programs', 'academics_calendar', 'academics_dept_detail',
        'students_admission', 'students_online_admission', 'students_fee_structure',
        'students_scholarship', 'students_library', 'students_alumni',
        'students_merit_list', 'students_syllabus',
        'naac_home', 'naac_iqac', 'naac_iiqa', 'naac_ssr', 'naac_dvv', 'naac_atr',
        'gallery_images', 'gallery_videos', 'gallery_news',
        'feedback_student', 'feedback_parent', 'feedback_faculty', 'feedback_alumni',
        'grievances_anti_ragging', 'grievances_icc', 'grievances_redressal',
        'grievances_submit', 'custom_page', 'infrastructure',
    ]
    breadcrumb_images = {k: _resolve(k) for k in _all_keys}

    try:
        from .utils import (
            get_navbar_menu,
            seed_default_menu_items,
            sync_facilities_menu_item,
            sync_event_feedback_menu_items,
        )
        seed_default_menu_items()
        sync_facilities_menu_item()
        sync_event_feedback_menu_items()
        navbar_menu = get_navbar_menu()
    except Exception:
        navbar_menu = []

    # Visitor counter logic
    visitor_count = 0
    try:
        from django.db.models import F
        from .models import VisitorCount
        vc, created = VisitorCount.objects.get_or_create(id=1)
        if not request.session.get('has_visited'):
            request.session['has_visited'] = True
            VisitorCount.objects.filter(id=1).update(count=F('count') + 1)
            vc.refresh_from_db()
        visitor_count = vc.count
    except Exception:
        pass

    return {
        'site_settings': settings_obj,
        'marquee_notices': combined_marquee,
        'important_links': important_links,
        'quick_links': quick_links,
        'breadcrumb_images': breadcrumb_images,
        'navbar_menu': navbar_menu,
        'visitor_count': visitor_count,
    }

