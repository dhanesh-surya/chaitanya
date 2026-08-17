from django.db import transaction


class _MenuChildren:
    def __init__(self, items):
        self._items = items

    def all(self):
        return self._items


class DynamicNavbarChild:
    """Navbar submenu item generated from Infrastructure records."""

    def __init__(self, title, url, open_in_new_tab=False):
        self.title = title
        self.url = url
        self.open_in_new_tab = open_in_new_tab
        self.is_named_url = False
        self.children = _MenuChildren([])

    def get_absolute_url(self):
        return self.url


class NavbarMenuItem:
    """Wraps a MenuItem and optionally injects dynamic submenu children."""

    def __init__(self, menu_item, children_override=None):
        self._menu_item = menu_item
        self._children_override = children_override

    def __getattr__(self, name):
        return getattr(self._menu_item, name)

    @property
    def children(self):
        if self._children_override is not None:
            return self._children_override
        return self._menu_item.children

    def get_absolute_url(self):
        return self._menu_item.get_absolute_url()


def sync_facilities_menu_item():
    """Ensure the top-level Facilities navbar item exists on every environment."""
    from .models import MenuItem

    facilities, created = MenuItem.objects.get_or_create(
        title='Facilities',
        parent=None,
        defaults={
            'url': 'core:infrastructure',
            'is_named_url': True,
            'open_in_new_tab': False,
            'order': 6,
            'is_active': True,
        },
    )

    if not created:
        updates = {}
        if facilities.url != 'core:infrastructure' or not facilities.is_named_url:
            updates['url'] = 'core:infrastructure'
            updates['is_named_url'] = True
        if not facilities.is_active:
            updates['is_active'] = True
        if updates:
            for field, value in updates.items():
                setattr(facilities, field, value)
            facilities.save(update_fields=list(updates.keys()))

    return facilities


def sync_event_feedback_menu_items():
    """
    Sync Feedback submenu with active event feedback campaigns (show_in_menu=True).
    Also ensures a list page link exists.
    """
    from .models import MenuItem

    try:
        from feedback.models import EventFeedbackCampaign
    except Exception:
        return

    feedback_parent = MenuItem.objects.filter(title='Feedback', parent=None).first()
    if not feedback_parent:
        return

    # List page
    list_item, _ = MenuItem.objects.get_or_create(
        title='Event Feedback Forms',
        parent=feedback_parent,
        defaults={
            'url': 'feedback:event_feedback_list',
            'is_named_url': True,
            'open_in_new_tab': False,
            'order': 5,
            'is_active': True,
        },
    )
    if list_item.url != 'feedback:event_feedback_list' or not list_item.is_named_url:
        list_item.url = 'feedback:event_feedback_list'
        list_item.is_named_url = True
        list_item.is_active = True
        list_item.save(update_fields=['url', 'is_named_url', 'is_active'])

    # Per-campaign links
    campaigns = EventFeedbackCampaign.objects.filter(show_in_menu=True, is_active=True)
    campaign_titles = set()
    base_order = 6
    for idx, campaign in enumerate(campaigns):
        title = (campaign.menu_title or campaign.title)[:120]
        campaign_titles.add(title)
        # Named URL with slug is not supported by MenuItem reverse without args,
        # so store the public path as a plain URL.
        public_path = campaign.get_public_url_path()
        item = MenuItem.objects.filter(parent=feedback_parent, title=title).first()
        if not item:
            # Also match by URL path
            item = MenuItem.objects.filter(
                parent=feedback_parent,
                url=public_path,
            ).first()
        if item:
            updates = {}
            if item.title != title:
                updates['title'] = title
            if item.url != public_path or item.is_named_url:
                updates['url'] = public_path
                updates['is_named_url'] = False
            if not item.is_active:
                updates['is_active'] = True
            order = base_order + idx
            if item.order != order:
                updates['order'] = order
            if updates:
                for field, value in updates.items():
                    setattr(item, field, value)
                item.save(update_fields=list(updates.keys()))
        else:
            MenuItem.objects.create(
                title=title,
                parent=feedback_parent,
                url=public_path,
                is_named_url=False,
                open_in_new_tab=False,
                order=base_order + idx,
                is_active=True,
            )

    # Deactivate menu items that pointed at event feedback paths no longer shown
    for item in MenuItem.objects.filter(parent=feedback_parent, is_named_url=False):
        if item.url and item.url.startswith('/feedback/events/') and item.url != '/feedback/events/':
            if item.title not in campaign_titles and item.title != 'Event Feedback Forms':
                if item.is_active:
                    item.is_active = False
                    item.save(update_fields=['is_active'])


def sync_admission_fest_feedback_menu_item():
    """Backward-compatible alias."""
    return sync_event_feedback_menu_items()


def get_navbar_menu():
    from django.urls import reverse

    from .models import Infrastructure, MenuItem

    menu_items = MenuItem.objects.filter(
        parent=None,
        is_active=True,
    ).prefetch_related('children', 'children__children')

    infrastructure_items = list(
        Infrastructure.objects.filter(is_active=True).order_by('order', 'title')
    )

    navbar_menu = []
    for menu in menu_items:
        if menu.title.strip().lower() == 'facilities' and infrastructure_items:
            dynamic_children = [
                DynamicNavbarChild(
                    title=infra.title,
                    url=infra.get_absolute_url(),
                )
                for infra in infrastructure_items
            ]
            navbar_menu.append(
                NavbarMenuItem(menu, children_override=_MenuChildren(dynamic_children))
            )
        else:
            navbar_menu.append(NavbarMenuItem(menu))

    return navbar_menu


def seed_default_menu_items():
    from .models import MenuItem

    if MenuItem.objects.exists():
        return

    # Structure: (title, url, is_named_url, open_in_new_tab, order, [children])
    defaults = [
        ("Home", "core:home", True, False, 1, []),
        
        ("About Us", "core:about", True, False, 2, [
            ("About Institute", "core:about", True, False, 1, []),
            ("Achievements & Recognition", "core:recognition", True, False, 2, []),
            ("Staff", "#", False, False, 3, [
                ("Teaching", "core:staff_teaching", True, False, 1, []),
                ("Non-Teaching", "core:staff_nonteaching", True, False, 2, [])
            ]),
            ("Committees", "core:committees", True, False, 4, []),
            ("Policies", "core:policies", True, False, 5, []),
            ("Infrastructure", "core:infrastructure", True, False, 6, []),
            ("Our Products", "core:products", True, False, 7, [])
        ]),
        
        ("Academics", "academics:programs", True, False, 3, [
            ("Arts", "#", False, False, 1, [
                ("Hindi", "academics:department_detail 'hindi'", True, False, 1, []),
                ("English", "academics:department_detail 'english'", True, False, 2, []),
                ("Sociology", "academics:department_detail 'sociology'", True, False, 3, []),
                ("Geography", "academics:department_detail 'geography'", True, False, 4, []),
                ("Social Work", "academics:department_detail 'social-work'", True, False, 5, []),
                ("Political Science", "academics:department_detail 'political-science'", True, False, 6, []),
                ("History", "academics:department_detail 'history'", True, False, 7, [])
            ]),
            ("Science", "#", False, False, 2, [
                ("Zoology", "academics:department_detail 'zoology'", True, False, 1, []),
                ("Physics", "academics:department_detail 'physics'", True, False, 2, []),
                ("Chemistry", "academics:department_detail 'chemistry'", True, False, 3, []),
                ("Mathematics", "academics:department_detail 'mathematics'", True, False, 4, []),
                ("Botany", "academics:department_detail 'botany'", True, False, 5, []),
                ("Forestry", "academics:department_detail 'forestry'", True, False, 6, []),
                ("Computer Science", "academics:department_detail 'computer-science'", True, False, 7, [])
            ]),
            ("Programs Offered", "academics:programs", True, False, 3, []),
            ("CO PO", "core:co_po", True, False, 4, []),
            ("Academic Calendar", "academics:academic_calendar", True, False, 5, [])
        ]),
        
        ("Student Corner", "students:admission", True, False, 4, [
            ("Admission Procedure", "students:admission", True, False, 1, []),
            ("University Admission", "https://www.snpvraigarh.in/", False, True, 2, []),
            ("Online Admission", "students:online_admission", True, False, 3, []),
            ("Fee Structure", "students:fee_structure", True, False, 4, []),
            ("Result", "https://www.snpvraigarh.in/", False, True, 5, []),
            ("Scholarship", "students:scholarship", True, False, 6, []),
            ("Library", "students:library", True, False, 7, []),
            ("Alumni", "students:alumni", True, False, 8, []),
            ("Merit List", "students:merit_list", True, False, 9, [])
        ]),
        
        ("NAAC", "naac:naac_home", True, False, 5, [
            ("NAAC", "naac:naac_home", True, False, 1, []),
            ("IQAC", "naac:iqac", True, False, 2, [
                ("IIQA", "naac:iiqa", True, False, 1, []),
                ("SSR", "naac:ssr", True, False, 2, []),
                ("DVV", "naac:dvv", True, False, 3, []),
                ("ATR", "naac:atr", True, False, 4, [])
            ])
        ]),
        
        ("Feedback", "#", False, False, 6, [
            ("Student's Feedback", "feedback:student_feedback", True, False, 1, []),
            ("Parent's Feedback", "feedback:parent_feedback", True, False, 2, []),
            ("Faculty's Feedback", "feedback:faculty_feedback", True, False, 3, []),
            ("Alumni's Feedback", "feedback:alumni_feedback", True, False, 4, []),
            ("Event Feedback Forms", "feedback:event_feedback_list", True, False, 5, []),
        ]),

        ("Facilities", "core:infrastructure", True, False, 6, []),
        
        ("Grievances", "#", False, False, 7, [
            ("Anti Ragging Committee", "grievances:anti_ragging", True, False, 1, []),
            ("Internal Complaints Committee (ICC)", "grievances:icc", True, False, 2, []),
            ("Grievance Redressal Committee", "grievances:redressal", True, False, 3, []),
            ("Submit a Grievance", "grievances:submit_grievance", True, False, 4, [])
        ]),
        
        ("UGC", "core:ugc", True, False, 8, []),
        
        ("Gallery", "#", False, False, 9, [
            ("Image Gallery", "gallery:image_gallery", True, False, 1, []),
            ("Video Gallery", "gallery:video_gallery", True, False, 2, []),
            ("News Gallery", "gallery:news_gallery", True, False, 3, [])
        ]),
        
        ("Student Login", "https://chaitanyapamgarh.onlineexamforms.com/student.aspx", False, True, 10, [])
    ]

    with transaction.atomic():
        def create_items(item_list, parent=None):
            for title, url, is_named_url, open_tab, order, children in item_list:
                item = MenuItem.objects.create(
                    title=title,
                    url=url,
                    is_named_url=is_named_url,
                    open_in_new_tab=open_tab,
                    order=order,
                    parent=parent
                )
                if children:
                    create_items(children, parent=item)

        create_items(defaults)
