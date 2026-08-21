from collections import OrderedDict

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.db import models
from .models import (
    BannerSlide, AccreditationLogo, StatCounter, CollegeInfo,
    Leadership, Committee, Policy, Achievement, Notice, ImportantLink,
    CareerGuidanceSubmission, SocialScheme, Testimonial, Event, Happening,
    QuickLinkCard, AboutPage, Recognition, UGCTable, UGCDocument,
    UGCPageSettings, UGCGrant, PopupAnnouncement,
    NSSPageSettings, NSSActivity, NSSGalleryImage,
    IICPageSettings, IICGalleryImage, CampusMedia, Infrastructure, Product, ProductInquiry, ProductCategory, ProductImage, ProductReview,
    MenuItem
)
from .forms import CareerGuidanceForm, ProductInquiryForm, ProductReviewForm, MenuItemForm
from gallery.models import GalleryItem


def home(request):
    banners = BannerSlide.objects.filter(is_active=True)
    logos = AccreditationLogo.objects.all()
    stats = StatCounter.objects.all()
    achievements = Achievement.objects.all()[:6]

    # Query new models
    social_schemes = SocialScheme.objects.all()
    testimonials = Testimonial.objects.all()
    events = Event.objects.filter(is_active=True)
    happenings = Happening.objects.order_by('-date', '-id')[:7]
    quick_link_cards = QuickLinkCard.objects.filter(is_active=True)
    campus_media = CampusMedia.objects.filter(is_active=True).order_by('order', 'id')

    # Query categorized notices
    latest_notices = Notice.objects.filter(is_active=True).order_by('-published_date')[:10]
    exam_notices = Notice.objects.filter(category='exam', is_active=True)[:10]
    admission_notices = Notice.objects.filter(category='admission', is_active=True)[:10]
    student_notices = Notice.objects.filter(category='students', is_active=True)[:10]

    # Query active homepage popup announcements (all active ones)
    active_popups = PopupAnnouncement.objects.filter(is_active=True)
    active_highlights = GalleryItem.objects.filter(is_active=True, is_homepage_highlight=True).order_by('order', '-date')

    # Query leadership messages
    principal = Leadership.objects.filter(role='principal').first()
    chairman = Leadership.objects.filter(role='chairman').first()
    director = Leadership.objects.filter(role='director').first()

    # Form handling
    if request.method == 'POST':
        form = CareerGuidanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your career guidance request has been submitted successfully!")
            return redirect('core:home')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = CareerGuidanceForm()

    context = {
        'banners': banners,
        'logos': logos,
        'stats': stats,
        'achievements': achievements,
        'social_schemes': social_schemes,
        'testimonials': testimonials,
        'events': events,
        'happenings': happenings,
        'quick_link_cards': quick_link_cards,
        'latest_notices': latest_notices,
        'exam_notices': exam_notices,
        'admission_notices': admission_notices,
        'student_notices': student_notices,
        'principal_member': principal,
        'chairman_member': chairman,
        'director_member': director,
        'form': form,
        'page_title': 'Home',
        'active_popups': active_popups,
        'active_highlights': active_highlights,
        'campus_media': campus_media,
    }
    return render(request, 'core/home.html', context)


def about(request):
    about_page = AboutPage.objects.first()
    if not about_page:
        # Pre-populate with exact text and image references from C:/temp-csac/chaitanyacg.ac.in/about/index.html
        about_page = AboutPage.objects.create(
            page_title="About Chaitanya Science and Arts College",
            breadcrumb_image="assets/images/banner/breadcrumb.png",
            about_us_title="About Us",
            about_us_description_1="Chaitanya Science and Arts College is located on National Highway (NH-49) in the heart of Pamgarh, Jangir Champa, Chhattisgarh. The College is governed by Chaitanya Shikshan Samiti. It is a premier academic institution in region catering to the needs of higher education since its inception in 2001. We pride ourselves on being a co-educational, multi-disciplinary institution, offering a diverse array of undergraduate and postgraduate programs, along with diploma courses spanning the realms of Natural Sciences, Humanities, Commerce, and Management.",
            about_us_description_2="We aim to deliver quality education of the quality in a conducive learning environment to cope up the challenges of higher education. Our overarching goal is to nurture the next generation of leaders, imbued with a spirit of critical inquiry, innovation, and entrepreneurship, poised to address the needs of our nation, and contribute to societal progress.",
            about_us_description_3="Our college possesses an extensive infrastructure meticulously crafted to accommodate both administrative and academic necessities. From vast playgrounds to inviting indoor-outdoor spaces, lush green gardens and a state-of-the-art auditorium, our campus offers a plethora of amenities designed to enrich the holistic educational experience.",
            about_us_image_url="https://chaitanyafiles01.s3.amazonaws.com/aboutImages/COLLEGE_BUILDING.jpg",
            stat1_value="8000+",
            stat1_label="Undergradute & Graduate Students",
            stat1_icon="assets/images/icon/11.svg",
            stat2_value="50+",
            stat2_label="Chaitanya College Faculty and Staff",
            stat2_icon="assets/images/icon/12.svg",
            stat3_value="5000+",
            stat3_label="Chaitanya College Alumni Worldwide",
            stat3_icon="assets/images/icon/13.svg",
            funfact1_value="90%",
            funfact1_label="Graduate success rate",
            funfact2_value="Top 10",
            funfact2_label="Colleges in CG that Create Futures",
            funfact3_value="No. 1",
            funfact3_label="In Innovation & Entrepreneurship",
            mission_statement="Our college is striving to provide a holistic environment to cater to the needs of its stakeholders by providing quality education and to accomplish its vision and mission.",
            vision_title="Vision",
            vision_text="To empower the youth from rural Chhattisgarh, especially those from economically disadvantaged backgrounds, by providing them with high-quality education and opportunities for professional growth, academic excellence, personal development, and social responsibility",
            mission_title="Mission",
            mission_text_1="To provide value-based quality education for the economically weaker section.",
            mission_text_2="To provide a learning environment that fosters academic excellence, personal, professional development, and social responsibility.",
            governance_title="Governance",
            governance_text="The College is governed by the “Governing Body” constituted as per college code with due recommendation of competent bodies. The governing body is chaired by Shri Veerendra Tiwari and members of the governing board as per guidelines. The Governing Body sincerely functions to achieve the vision and mission of the institution. The meetings of governing body are regularly organized to formulate strategies to implement guidelines of National Education Policy (NEP-2020), Department of Higher Education, Chhattisgarh Govt., and Affiliating University. In the leadership of the Governing body various initiatives are being taken for effective implementation and execution of desired guidelines to bring institutional distinctiveness by adding to its quality and excellence. The committee administers the institution through participative management and decentralization to inculcate a culture of amicable ambience in the campus. As per recent guidelines of new education policy e-governance and use of ICT (LMS) in teaching learning process has been implemented to bring accuracy, transparency, and fastness to make the governance efficient and accessible.",
            features_title="Distinctive Features of the College",
            features_list="Multidisciplinary Institution\nHolistic Environment for Teaching & Learning\nUse of ICT/LMS & Experiential Learning Pedagogies\nConduction of value-added courses/ workshops/ capacity building and skill development programs/ seminars/ outreach programs\nPromotion for research activities. Recognized Research Center of Geography\nSignificant achievements are evidenced in the merit list of the university\nE-Governance\nMentoring of students by faculty members and specialists.\nCentral Library with access for digital resources viz. INFLIBNET/SWAYM/EPATHSHALA/MOOCS/NPTL/NDL\nSpecious properly ventilated classrooms equipped with online & offline facilities\nWell-developed scientific laboratories to support undergraduate & postgraduate syllabus\nAn advanced computer center\nWi-Fi Campus\nLush green vast campus with gardens providing natural ecological setting\nHerbal garden having diversity of more than 150 species of medicinal plants serving the educative purpose\nPlayground for various games and athletics\nLife style management and YOGIC practices are being promoted to foster optimal learning environment in the campus.\nAuditorium equipped for academic conferences and cultural programs\nSignificant achievements in the social service and community development by active participation of NSS unit and other students of the college\nDistinguished alumni of the College are our asset.\nCleanliness in the campus maintenance of health and hygiene, blood donation",
            testimonial_text="Welcome to Chaitanya Science and Arts College, where we provide high-quality education to empower rural youth and foster academic and personal growth. Our goal is to help students achieve excellence and contribute positively to society. We are committed to nurturing innovation, critical thinking, and leadership skills in every student.",
            testimonial_author="VK Gupta",
            testimonial_author_image=None
        )

    features = [f.strip() for f in about_page.features_list.split('\n') if f.strip()]
    leadership_members = Leadership.objects.all().order_by('order', 'id')
    context = {
        'about': about_page,
        'features': features,
        'leadership_members': leadership_members,
        'page_title': 'About Us',
        'breadcrumb': about_page.page_title,
    }
    return render(request, 'core/about.html', context)






def committees(request):
    committees_list = Committee.objects.prefetch_related('members').all()
    context = {
        'committees': committees_list,
        'page_title': 'Committees',
        'breadcrumb': 'Committees',
    }
    return render(request, 'core/committees.html', context)


def committee_detail(request, slug):
    from django.shortcuts import get_object_or_404
    committee = get_object_or_404(Committee, slug=slug)
    members = committee.members.all().order_by('order')
    activities = committee.activities.all().order_by('order', '-date')
    gallery_images = committee.gallery_images.all().order_by('order')
    
    context = {
        'committee': committee,
        'members': members,
        'activities': activities,
        'gallery_images': gallery_images,
        'page_title': committee.name,
        'breadcrumb': committee.name,
    }
    return render(request, 'core/committee_detail.html', context)


def policies(request):
    policies_list = Policy.objects.all()
    context = {
        'policies': policies_list,
        'page_title': 'Policies',
        'breadcrumb': 'Policies',
    }
    return render(request, 'core/policies.html', context)


def recognition(request):
    recognitions = Recognition.objects.all().order_by('order')
    achievements = Achievement.objects.all().order_by('order')
    context = {
        'recognitions': recognitions,
        'achievements': achievements,
        'page_title': 'Achievements & Recognition',
        'breadcrumb': 'Achievements & Recognition',
    }
    return render(request, 'core/recognition.html', context)


def staff_teaching(request):
    from academics.models import Department, DepartmentFaculty
    from .models import TeachingStaffPageSettings

    page_settings, _ = TeachingStaffPageSettings.objects.get_or_create(pk=1)

    faculty_groups = []
    departments = (
        Department.objects.filter(faculty__isnull=False)
        .distinct()
        .order_by('order', 'name')
    )
    for department in departments:
        members = (
            DepartmentFaculty.objects.filter(department=department)
            .select_related('department')
            .order_by('order', 'name')
        )
        if members.exists():
            faculty_groups.append({
                'department': department,
                'members': members,
            })

    context = {
        'faculty_groups': faculty_groups,
        'page_settings': page_settings,
        'page_title': 'Teaching Staff',
        'breadcrumb': 'Teaching Staff',
    }
    return render(request, 'core/staff_teaching.html', context)


def staff_nonteaching(request):
    from .models import NonTeachingStaffPageSettings, NonTeachingStaffMember

    page_settings, _ = NonTeachingStaffPageSettings.objects.get_or_create(pk=1)
    staff_members = NonTeachingStaffMember.objects.filter(is_active=True)

    context = {
        'page_settings': page_settings,
        'staff_members': staff_members,
        'page_title': 'Non-Teaching Staff',
        'breadcrumb': 'Non-Teaching Staff',
    }
    return render(request, 'core/staff_nonteaching.html', context)


def notices(request):
    latest_notices = Notice.objects.filter(is_active=True)
    exam_notices = Notice.objects.filter(category='exam', is_active=True)
    admission_notices = Notice.objects.filter(category='admission', is_active=True)
    student_notices = Notice.objects.filter(category='students', is_active=True)
    
    context = {
        'latest_notices': latest_notices,
        'exam_notices': exam_notices,
        'admission_notices': admission_notices,
        'student_notices': student_notices,
        'page_title': 'Notices',
        'breadcrumb': 'Notices & Announcements',
    }
    return render(request, 'core/notices.html', context)


def contact(request):
    from .models import SiteSettings
    settings_obj = SiteSettings.objects.first()
    context = {
        'settings': settings_obj,
        'page_title': 'Contact Us',
        'breadcrumb': 'Contact Us',
    }
    return render(request, 'core/contact.html', context)


def nss(request):
    nss_settings = NSSPageSettings.objects.first()
    if not nss_settings:
        nss_settings = NSSPageSettings.objects.create(
            banner_title="National Service Scheme Chaitanya Science and Arts College, Pamgarh",
            banner_description="The NSS symbol is based on the 'Rath Wheel' of the Konark Sun Temple of Orissa. The giant wheel portrays the cycles of creation, preservation and release and signifies the movement in life across time and space. The design of the symbol, a simplified form of Sun Chariot Wheel primarily depicts movement. The wheel signifies the progressive cycle of life. It also stands for dynamism and progressive outlook of youth.",
            banner_image_url="nss/background.jpg",
            banner_icon_url="nss/nss.svg"
        )
        # Prepopulate default activities
        default_activities = [
            ("01", "Free medical campus at various and needy villages", "fa-user-md"),
            ("02", "Dental camp, Health camp & Eye camp", "fa-tooth"),
            ("03", "Personality development programs", "fa-users"),
            ("04", "NSS volunteers participation and performance in skit, dance and drama", "fa-theater-masks"),
            ("05", "Counselling sessions and medical advice", "fa-comments"),
            ("06", "Conducting Traffic awareness events", "fa-traffic-light"),
            ("07", "Conducted rallies for different social awareness themes in association with other social organizations", "fa-bullhorn"),
            ("08", "Tree plantation and helping the people to do so frequently", "fa-tree"),
            ("09", "Special camps for road safety measures", "fa-shield-halved"),
        ]
        for i, (sn, title, icon) in enumerate(default_activities):
            NSSActivity.objects.get_or_create(
                serial_number=sn,
                title=title,
                defaults={'fa_icon': icon, 'order': i}
            )
        # Prepopulate default gallery images
        default_gallery = [
            "Beti_Bachao_2.jpeg",
            "15.png",
            "17.png",
            "14.png",
            "16.png",
            "13.png",
            "WhatsApp_Image_2025-09-13_at_10.43.52_AM_1.jpeg",
            "WhatsApp_Image_2025-09-20_at_7.37.05_AM.jpeg",
            "WhatsApp_Image_2025-09-26_at_10.43.16_16bce940.jpg",
        ]
        for i, filename in enumerate(default_gallery):
            NSSGalleryImage.objects.get_or_create(
                image=f"nss/gallery/{filename}",
                defaults={'caption': filename.split('.')[0].replace('_', ' '), 'order': i}
            )
        # Mark existing happenings with "NSS" or matching IDs as NSS Activity
        nss_ids = [2, 9, 31, 133, 93, 80, 77, 20, 70, 57, 81, 58, 69, 62, 60, 63, 55, 7, 52, 65, 5, 13, 64, 74, 72, 54, 101, 21, 28, 121, 124, 125, 122, 129, 136, 131, 145]
        from django.db.models import Q
        Happening.objects.filter(
            Q(id__in=nss_ids) | Q(title__icontains="nss") | Q(title__icontains="national service scheme")
        ).update(is_nss_activity=True)

    # Query activities, gallery, and happenings
    activities = NSSActivity.objects.all().order_by('order', 'serial_number')
    gallery_images = NSSGalleryImage.objects.all().order_by('order', 'id')
    nss_happenings = Happening.objects.filter(is_nss_activity=True).order_by('-date', '-id')

    context = {
        'nss_settings': nss_settings,
        'activities': activities,
        'gallery_images': gallery_images,
        'nss_happenings': nss_happenings,
        'page_title': 'NSS',
        'breadcrumb': 'National Service Scheme (NSS)',
    }
    return render(request, 'core/nss.html', context)


def iic(request):
    settings_obj = IICPageSettings.objects.first()
    if not settings_obj:
        settings_obj = IICPageSettings.objects.create(
            title="INSTITUTION'S INNOVATION COUNCIL (IIC)",
            sub_title="Ministry of Education Supported",
            description="In the year 2018, the Ministry of Education (MoE) through MoE’s Innovation Cell (MIC) launched the Institution’s Innovation Council (IIC) program in collaboration with AICTE for Higher Educational Institutions (HEIs) to systematically foster the culture of innovation and start-up ecosystem in education institutions. Primarily, IIC’s role is to engage large number of faculty, students and staff in various innovation and entrepreneurship related activities such as ideation, Problem solving, Proof of Concept development, Design Thinking, IPR, project handling and management at Pre-incubation/Incubation stage, etc., so that innovation and entrepreneurship ecosystem gets established and stabilized in HEIs.",
            about_image_1="iic/about_3.png",
            about_image_2="iic/about_4.png"
        )
        
        default_gallery = [
            ("news_1.jpg", "News 1"),
            ("Workshop_1.jpeg", "Workshop 1"),
            ("IMG-20240326-WA0008.jpg", "Activity 1"),
            ("iic3.png", "IIC Certificate 3"),
            ("iic2.png", "IIC Certificate 2"),
            ("iic1.png", "IIC Certificate 1"),
            ("WhatsApp_Image_2024-10-05_at_1.37.18_PM_1.jpeg", "Activity 2"),
            ("WhatsApp_Image_2024-10-05_at_1.37.20_PM.jpeg", "Activity 3"),
            ("cr1.jpeg", "Activity 4"),
            ("cr3.jpeg", "Activity 5"),
            ("WhatsApp_Image_2024-10-01_at_5.07.44_PM_1.jpeg", "Activity 6"),
            ("IMG_20241009_134505156.jpg", "Activity 7"),
            ("paper_6.jpg", "Paper Clipping 6"),
            ("news_paper_11.jpg", "Paper Clipping 11"),
        ]
        for i, (filename, caption) in enumerate(default_gallery):
            IICGalleryImage.objects.get_or_create(
                image=f"iic/gallery/{filename}",
                defaults={'caption': caption, 'order': i}
            )
            
        iic_happenings_ids = [1, 4, 11, 47, 68, 103, 107, 108, 110, 111, 113, 118, 127, 135]
        Happening.objects.filter(id__in=iic_happenings_ids).update(is_iic_activity=True)

    gallery_images = IICGalleryImage.objects.all().order_by('order', 'id')
    happenings_list = Happening.objects.filter(is_iic_activity=True).order_by('-date', '-id')

    context = {
        'settings': settings_obj,
        'gallery_images': gallery_images,
        'happenings': happenings_list,
        'page_title': 'IIC',
        'breadcrumb': 'Institution Innovation Council (IIC)',
    }
    return render(request, 'core/iic.html', context)


def ugc(request):
    page_settings = UGCPageSettings.objects.first()
    if not page_settings:
        page_settings = UGCPageSettings.objects.create()
    
    benefits = [b.strip() for b in page_settings.benefits_list.split('\n') if b.strip()]
    grants = UGCGrant.objects.filter(is_active=True).order_by('order', 'id')
    ugc_tables = UGCTable.objects.filter(is_active=True).prefetch_related('documents')
    
    context = {
        'page_settings': page_settings,
        'benefits': benefits,
        'grants': grants,
        'ugc_tables': ugc_tables,
        'page_title': 'UGC',
        'breadcrumb': 'University Grants Commission (UGC)',
    }
    return render(request, 'core/ugc.html', context)


def nep(request):
    from .models import NEPTab
    nep_tabs = NEPTab.objects.filter(is_active=True).prefetch_related('files', 'links').order_by('order', 'title')
    context = {
        'page_title': 'NEP 2020',
        'breadcrumb': 'National Education Policy 2020',
        'nep_tabs': nep_tabs,
    }
    return render(request, 'core/nep.html', context)




def sports(request):
    from .models import SportsPageSettings, SportsGalleryImage
    from django.utils import timezone

    # Get or create singleton settings
    settings_obj, _ = SportsPageSettings.objects.get_or_create(pk=1)

    # Sports-tagged notices
    sports_notices = Notice.objects.filter(
        category='sports', is_active=True
    ).order_by('-published_date')[:10]

    # Sports-tagged upcoming events (sorted by date, show upcoming + recent)
    sports_events = Event.objects.filter(
        is_sports_event=True, is_active=True
    ).order_by('date')[:8]

    # Sports gallery
    gallery_images = SportsGalleryImage.objects.filter(is_active=True)

    # Sports happenings (past activities)
    sports_happenings = Happening.objects.filter(
        is_sports_activity=True
    ).order_by('-date')[:6]

    context = {
        'page_title': 'Sports',
        'breadcrumb': 'Sports & Athletics',
        'settings': settings_obj,
        'facilities': settings_obj.get_facilities_list(),
        'achievements': settings_obj.get_achievements_list(),
        'policies': settings_obj.get_policies_list(),
        'sports_notices': sports_notices,
        'sports_events': sports_events,
        'gallery_images': gallery_images,
        'sports_happenings': sports_happenings,
        'today': timezone.now().date(),
    }
    return render(request, 'core/sports.html', context)


def co_po(request):
    from academics.models import COPOMapping, Department
    departments = Department.objects.prefetch_related('copo_mappings').all()
    context = {
        'departments': departments,
        'page_title': 'CO-PO Mapping',
        'breadcrumb': 'Course Outcomes & Program Outcomes',
    }
    return render(request, 'core/co_po.html', context)


def happenings(request):
    from django.core.paginator import Paginator
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    year = request.GET.get('year', '')
    month = request.GET.get('month', '')

    happenings_list = Happening.objects.all()

    if query:
        happenings_list = happenings_list.filter(
            models.Q(title__icontains=query) | models.Q(category__icontains=query)
        )
    if category:
        happenings_list = happenings_list.filter(category=category)
    if year:
        happenings_list = happenings_list.filter(date__year=int(year))
    if month:
        happenings_list = happenings_list.filter(date__month=int(month))

    paginator = Paginator(happenings_list, 12)  # 12 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Build filter option lists
    all_categories = (
        Happening.objects.exclude(category__isnull=True)
        .exclude(category='')
        .values_list('category', flat=True)
        .distinct()
        .order_by('category')
    )
    all_years = [
        d.year for d in
        Happening.objects.exclude(date__isnull=True)
        .dates('date', 'year', order='DESC')
    ]
    month_choices = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December'),
    ]

    context = {
        'page_obj': page_obj,
        'query': query,
        'selected_category': category,
        'selected_year': year,
        'selected_month': month,
        'all_categories': all_categories,
        'all_years': all_years,
        'month_choices': month_choices,
        'page_title': 'Recent Happenings',
        'breadcrumb': 'Recent Happenings',
    }
    return render(request, 'core/happenings.html', context)


def happening_detail(request, pk):
    from django.shortcuts import get_object_or_404
    happening = get_object_or_404(Happening, pk=pk)
    gallery_images = happening.gallery_images.all()
    
    context = {
        'happening': happening,
        'gallery_images': gallery_images,
        'page_title': happening.title,
        'breadcrumb': happening.title,
    }
    return render(request, 'core/happening_detail.html', context)


def event_detail(request, pk):
    from django.shortcuts import get_object_or_404
    event = get_object_or_404(Event, pk=pk, is_active=True)
    
    context = {
        'event': event,
        'page_title': event.title,
        'breadcrumb': 'Event Details',
    }
    return render(request, 'core/event_detail.html', context)


def infrastructure(request):
    infrastructure_list = Infrastructure.objects.filter(is_active=True).prefetch_related('images').order_by('order', 'title')
    
    # If no data exists, pre-populate with default mock data for a stunning initial look
    if not infrastructure_list.exists():
        from .models import InfrastructureImage
        s1 = Infrastructure.objects.create(
            title="Scientific Laboratories",
            description="Our state-of-the-art laboratories are fully equipped with advanced modern instruments to cater to both undergraduate and postgraduate course requirements. Each lab is properly ventilated, spacious, and designed with optimal safety features, allowing students to conduct research, experiments, and practical studies under expert mentorship. Specializations include Chemistry, Physics, Botany, Zoology, and Forestry.",
            video_url="https://www.youtube.com/watch?v=NwbCZVm1exI",
            order=1
        )
        InfrastructureImage.objects.create(
            infrastructure=s1,
            image_url="https://chaitanyafiles01.s3.amazonaws.com/aboutImages/COLLEGE_BUILDING.jpg",
            caption="Advanced Chemistry Laboratory",
            order=1
        )
        InfrastructureImage.objects.create(
            infrastructure=s1,
            image_url="https://chaitanyafiles01.s3.amazonaws.com/aboutImages/COLLEGE_BUILDING.jpg",
            caption="Physics Instrumentation Room",
            order=2
        )

        s2 = Infrastructure.objects.create(
            title="Central Digital Library",
            description="The Central Library serves as the academic heart of the institution, housing a comprehensive collection of over 15,000 reference books, journals, textbooks, and encyclopedias. Equipped with high-speed internet connectivity, the digital section provides students and faculty with seamless access to premium databases and resources, including INFLIBNET, SWAYAM, e-Pathshala, MOOCs, and the National Digital Library (NDL).",
            video_url="",
            order=2
        )
        InfrastructureImage.objects.create(
            infrastructure=s2,
            image_url="https://chaitanyafiles01.s3.amazonaws.com/aboutImages/COLLEGE_BUILDING.jpg",
            caption="Main Reading Hall & Book Stacks",
            order=1
        )
        InfrastructureImage.objects.create(
            infrastructure=s2,
            image_url="https://chaitanyafiles01.s3.amazonaws.com/aboutImages/COLLEGE_BUILDING.jpg",
            caption="Digital Library & E-Resource Access Terminals",
            order=2
        )

        s3 = Infrastructure.objects.create(
            title="Advanced Computer Center",
            description="Our advanced Computer Center is designed to support the growing digital needs of all academic streams. Equipped with the latest workstations, enterprise-grade software, and high-speed Wi-Fi, the lab provides an ideal environment for programming, database management, web development, and digital literacy. Regular workshops on emerging tech (Python, Web Tech) are conducted here.",
            video_url="",
            order=3
        )
        InfrastructureImage.objects.create(
            infrastructure=s3,
            image_url="https://chaitanyafiles01.s3.amazonaws.com/aboutImages/COLLEGE_BUILDING.jpg",
            caption="Main Computer Lab",
            order=1
        )
        
        infrastructure_list = Infrastructure.objects.filter(is_active=True).prefetch_related('images').order_by('order', 'title')

    context = {
        'infrastructure_list': infrastructure_list,
        'page_title': 'Campus Infrastructure',
        'breadcrumb': 'Infrastructure',
    }
    return render(request, 'core/infrastructure.html', context)


def _group_infrastructure_images(images):
    """Group infrastructure images by caption/subcategory for the detail page."""
    groups = OrderedDict()
    for image in images:
        label = image.caption.strip() if image.caption else 'Facility Gallery'
        if label not in groups:
            groups[label] = {
                'caption': label,
                'description': image.description.strip() if image.description else '',
                'images': [],
            }
        groups[label]['images'].append(image)
        if image.description and not groups[label]['description']:
            groups[label]['description'] = image.description.strip()
    return list(groups.values())


def infrastructure_detail(request, slug):
    infrastructure_item = get_object_or_404(
        Infrastructure.objects.prefetch_related('images'),
        slug=slug,
        is_active=True,
    )
    image_groups = _group_infrastructure_images(infrastructure_item.images.all())
    related_infrastructure = (
        Infrastructure.objects.filter(is_active=True)
        .exclude(pk=infrastructure_item.pk)
        .order_by('order', 'title')[:6]
    )

    context = {
        'infrastructure_item': infrastructure_item,
        'image_groups': image_groups,
        'image_count': infrastructure_item.images.count(),
        'subcategory_count': len(image_groups),
        'related_infrastructure': related_infrastructure,
        'page_title': infrastructure_item.title,
        'breadcrumb': infrastructure_item.title,
    }
    return render(request, 'core/infrastructure_detail.html', context)


def products(request):
    products_list = Product.objects.filter(is_active=True).order_by('order', '-created_at')

    # Seed data if blank
    if not products_list.exists():
        c_apparel, _ = ProductCategory.objects.get_or_create(name="Apparel")
        c_drinkware, _ = ProductCategory.objects.get_or_create(name="Drinkware")
        c_stationery, _ = ProductCategory.objects.get_or_create(name="Stationery")
        Product.objects.create(
            category=c_drinkware,
            name="Chaitanya College Premium Mug",
            description="High-quality ceramic coffee mug featuring the official college crest. Perfect for campus desks and alumni collection.",
            price=150.00,
            image_url="https://i.postimg.cc/k5Z5snNv/csac-naac.png",
            in_stock=True,
            order=1
        )
        Product.objects.create(
            category=c_apparel,
            name="CSAC Classic Cotton T-Shirt",
            description="Super-soft 100% cotton crewneck t-shirt featuring the college branding. Available in multiple sizes.",
            price=350.00,
            image_url="https://i.postimg.cc/k5Z5snNv/csac-naac.png",
            in_stock=True,
            order=2
        )
        Product.objects.create(
            category=c_stationery,
            name="Academic Planner & Notebook Set",
            description="Premium hardbound notebook and academic planner to track classes, schedules, and research notes.",
            price=200.00,
            image_url="https://i.postimg.cc/k5Z5snNv/csac-naac.png",
            in_stock=False,
            order=3
        )
        products_list = Product.objects.filter(is_active=True).order_by('order', '-created_at')

    # Category Filtering logic
    categories = ProductCategory.objects.all().order_by('order', 'name')
    selected_category_slug = request.GET.get('category', '')

    # Handle purchase interest form submission (fallback from card directly)
    if request.method == 'POST':
        form = ProductInquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your purchase interest has been submitted. Our team will contact you soon.")
            return redirect('core:products')
        else:
            messages.error(request, "Failed to submit interest. Please correct form details.")
    else:
        form = ProductInquiryForm()

    context = {
        'products': products_list,
        'categories': categories,
        'selected_category_slug': selected_category_slug,
        'form': form,
        'page_title': 'Our Products',
        'breadcrumb': 'Our Products',
    }
    return render(request, 'core/products.html', context)


def product_detail(request, slug):
    from django.shortcuts import get_object_or_404
    product = get_object_or_404(Product, slug=slug, is_active=True)
    reviews = product.reviews.filter(is_approved=True).order_by('-created_at')
    images = product.images.all().order_by('order')

    # Calculate average rating
    rating_range = range(1, 6)
    avg_rating = 0
    if reviews.exists():
        total_rating = sum(r.rating for r in reviews)
        avg_rating = round(total_rating / reviews.count(), 1)
        avg_rating_int = int(round(avg_rating))
    else:
        avg_rating_int = 0

    # Initialize Forms
    inquiry_form = ProductInquiryForm(initial={'product': product})
    review_form = ProductReviewForm()

    if request.method == 'POST':
        if 'reviewer_name' in request.POST:
            # Review form submission
            review_form = ProductReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.product = product
                review.save()
                messages.success(request, "Your review has been submitted successfully!")
                return redirect('core:product_detail', slug=product.slug)
            else:
                messages.error(request, "Failed to submit review. Please check the form fields.")
        else:
            # Inquiry/Buy form submission
            inquiry_form = ProductInquiryForm(request.POST)
            if inquiry_form.is_valid():
                inquiry_form.save()
                messages.success(request, "Thank you! Your purchase interest has been submitted. Our team will contact you soon.")
                return redirect('core:product_detail', slug=product.slug)
            else:
                messages.error(request, "Failed to submit interest. Please check the inquiry form fields.")

    context = {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'avg_rating_int': avg_rating_int,
        'rating_range': rating_range,
        'images': images,
        'inquiry_form': inquiry_form,
        'review_form': review_form,
        'page_title': product.name,
        'breadcrumb': 'Our Products',
    }
    return render(request, 'core/product_detail.html', context)


def library(request):
    from .models import LibraryPageSettings, LibraryBookCategory, LibraryResource, LibraryBookSuggestion
    from .forms import LibraryBookSuggestionForm
    from django.contrib import messages
    from django.shortcuts import redirect, render

    # Get settings or create default
    settings_obj = LibraryPageSettings.objects.first()
    if not settings_obj:
        settings_obj = LibraryPageSettings.objects.create()

    # Get categories & resources
    categories = LibraryBookCategory.objects.all().order_by('order', 'id')
    resources = LibraryResource.objects.all().order_by('order', 'id')

    # Handle Suggestion Form submission
    if request.method == 'POST':
        form = LibraryBookSuggestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your book recommendation has been submitted successfully to the Library Committee.")
            return redirect('core:library')
        else:
            messages.error(request, "Failed to submit recommendation. Please correct the fields below.")
    else:
        form = LibraryBookSuggestionForm()

    context = {
        'page_title': 'Library',
        'breadcrumb': 'Smt. Urmila Devi Smriti Pustkaalaya',
        'settings': settings_obj,
        'sections': settings_obj.get_sections_list(),
        'categories': categories,
        'resources': resources,
        'form': form,
    }
    return render(request, 'core/library.html', context)


def sitemap(request):
    context = {
        'page_title': 'Sitemap',
        'breadcrumb': 'Website Sitemap',
    }
    return render(request, 'core/sitemap.html', context)


from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404

def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='/admin/login/')(view_func)

@staff_required
def manage_navbar(request):
    from .utils import seed_default_menu_items
    seed_default_menu_items()
    
    menu_items = MenuItem.objects.filter(parent=None).prefetch_related('children', 'children__children')
    form = MenuItemForm()
    
    context = {
        'menu_items': menu_items,
        'form': form,
        'page_title': 'Manage Navigation Bar',
        'breadcrumb': 'Manage Navbar',
    }
    return render(request, 'core/manage_navbar.html', context)

@staff_required
def add_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Navbar menu item added successfully!")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    return redirect('core:manage_navbar')

@staff_required
def edit_menu_item(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"Navbar menu item '{item.title}' updated successfully!")
            return redirect('core:manage_navbar')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        form = MenuItemForm(instance=item)
        
    context = {
        'form': form,
        'item': item,
        'page_title': f"Edit Menu Item: {item.title}",
        'breadcrumb': "Edit Menu Item",
    }
    return render(request, 'core/edit_menu_item.html', context)

@staff_required
def delete_menu_item(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    title = item.title
    item.delete()
    messages.success(request, f"Navbar menu item '{title}' and all its submenus were removed successfully.")
    return redirect('core:manage_navbar')

@staff_required
def move_menu_item(request, pk, direction):
    item = get_object_or_404(MenuItem, pk=pk)
    siblings = list(MenuItem.objects.filter(parent=item.parent).order_by('order', 'id'))
    
    # Re-index sibling orders from 1 to N to prevent overlapping order values
    for idx, sib in enumerate(siblings):
        sib.order = idx + 1
        sib.save()
        
    # Find current item index
    try:
        curr_idx = next(i for i, sib in enumerate(siblings) if sib.pk == item.pk)
    except StopIteration:
        curr_idx = -1
        
    if curr_idx != -1:
        if direction == 'up' and curr_idx > 0:
            siblings[curr_idx].order, siblings[curr_idx - 1].order = siblings[curr_idx - 1].order, siblings[curr_idx].order
            siblings[curr_idx].save()
            siblings[curr_idx - 1].save()
            messages.success(request, f"Moved '{item.title}' up.")
        elif direction == 'down' and curr_idx < len(siblings) - 1:
            siblings[curr_idx].order, siblings[curr_idx + 1].order = siblings[curr_idx + 1].order, siblings[curr_idx].order
            siblings[curr_idx].save()
            siblings[curr_idx + 1].save()
            messages.success(request, f"Moved '{item.title}' down.")
            
    return redirect('core:manage_navbar')


@staff_required
def edit_leadership(request, role):
    if role not in ['director', 'chairman', 'principal']:
        return redirect('core:home')
        
    from .models import Leadership
    from .forms import LeadershipForm
    
    member = Leadership.objects.filter(role=role).first()
    if not member:
        # Pre-populate defaults if none exists
        if role == 'director':
            name = 'Mr Veerendra Tiwari'
            msg = 'Welcome to Chaitanya Science and Arts College, where our mission is to empower rural youth, especially those from economically disadvantaged backgrounds, with high-quality education. We are dedicated to fostering academic excellence, personal growth, and social responsibility in our students. Together, we aim to build a brighter future for individuals and the community.'
        elif role == 'chairman':
            name = 'Mr Veerendra Tiwari'
            msg = 'Welcome to Chaitanya Science and Arts College, where our mission is to empower rural youth, especially those from economically disadvantaged backgrounds, with high-quality education. We are dedicated to fostering academic excellence, personal growth, and social responsibility in our students. Together, we aim to build a brighter future for individuals and the community.'
        else:
            name = 'Dr Vinod Kumar Gupta'
            msg = 'Welcome to Chaitanya Science and Arts College, where we provide high-quality education to empower rural youth and foster academic and personal growth. Our goal is to help students achieve excellence and contribute positively to society. We are committed to nurturing innovation, critical thinking, and leadership skills in every student.'
            
        member = Leadership.objects.create(
            role=role,
            name=name,
            message=msg
        )
        
    if request.method == 'POST':
        form = LeadershipForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, f"{member.get_role_display()} message updated successfully!")
            return redirect('core:home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        form = LeadershipForm(instance=member)
        
    context = {
        'form': form,
        'member': member,
        'page_title': f"Edit {member.get_role_display()} Message",
        'breadcrumb': f"Edit {member.get_role_display()}",
    }
    return render(request, 'core/edit_leadership.html', context)


@staff_required
def edit_teaching_staff_page(request):
    from .models import TeachingStaffPageSettings
    from .forms import TeachingStaffPageSettingsForm

    page_settings, _ = TeachingStaffPageSettings.objects.get_or_create(pk=1)

    if request.method == 'POST':
        form = TeachingStaffPageSettingsForm(request.POST, instance=page_settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teaching staff page content updated successfully!')
            return redirect('core:staff_teaching')
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"Error in {field}: {error}")
    else:
        form = TeachingStaffPageSettingsForm(instance=page_settings)

    context = {
        'form': form,
        'page_settings': page_settings,
        'page_title': 'Edit Teaching Staff Page',
        'breadcrumb': 'Edit Teaching Staff Page',
    }
    return render(request, 'core/edit_teaching_staff_page.html', context)


@staff_required
def edit_nonteaching_staff_page(request):
    from .models import NonTeachingStaffPageSettings
    from .forms import NonTeachingStaffPageSettingsForm

    page_settings, _ = NonTeachingStaffPageSettings.objects.get_or_create(pk=1)

    if request.method == 'POST':
        form = NonTeachingStaffPageSettingsForm(request.POST, instance=page_settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Non-teaching staff page content updated successfully!')
            return redirect('core:staff_nonteaching')
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"Error in {field}: {error}")
    else:
        form = NonTeachingStaffPageSettingsForm(instance=page_settings)

    context = {
        'form': form,
        'page_settings': page_settings,
        'page_title': 'Edit Non-Teaching Staff Page',
        'breadcrumb': 'Edit Non-Teaching Staff Page',
    }
    return render(request, 'core/edit_nonteaching_staff_page.html', context)


@staff_required
def manage_nonteaching_staff(request):
    from .models import NonTeachingStaffMember
    from .forms import NonTeachingStaffMemberForm

    if request.method == 'POST':
        form = NonTeachingStaffMemberForm(request.POST)
        if form.is_valid():
            member = form.save()
            messages.success(request, f"Staff member '{member.name}' added successfully!")
            return redirect('core:manage_nonteaching_staff')
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"Error in {field}: {error}")
    else:
        form = NonTeachingStaffMemberForm()

    staff_members = NonTeachingStaffMember.objects.all()

    context = {
        'form': form,
        'staff_members': staff_members,
        'page_title': 'Manage Non-Teaching Staff',
        'breadcrumb': 'Manage Non-Teaching Staff',
    }
    return render(request, 'core/manage_nonteaching_staff.html', context)


@staff_required
def edit_nonteaching_staff_member(request, pk):
    from .models import NonTeachingStaffMember
    from .forms import NonTeachingStaffMemberForm

    member = get_object_or_404(NonTeachingStaffMember, pk=pk)

    if request.method == 'POST':
        form = NonTeachingStaffMemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, f"Staff member '{member.name}' updated successfully!")
            return redirect('core:manage_nonteaching_staff')
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"Error in {field}: {error}")
    else:
        form = NonTeachingStaffMemberForm(instance=member)

    context = {
        'form': form,
        'member': member,
        'page_title': 'Edit Staff Member',
        'breadcrumb': 'Edit Staff Member',
    }
    return render(request, 'core/edit_nonteaching_staff_member.html', context)


@staff_required
def delete_nonteaching_staff_member(request, pk):
    from .models import NonTeachingStaffMember

    member = get_object_or_404(NonTeachingStaffMember, pk=pk)
    if request.method == 'POST':
        name = member.name
        member.delete()
        messages.success(request, f"Staff member '{name}' deleted successfully!")
    return redirect('core:manage_nonteaching_staff')


@staff_required
def manage_documents(request):
    from .models import UploadedDocument
    from .forms import UploadedDocumentForm
    
    if request.method == 'POST':
        form = UploadedDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save()
            messages.success(request, f"Document '{doc.title}' uploaded successfully!")
            return redirect('core:manage_documents')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        form = UploadedDocumentForm()
        
    documents = UploadedDocument.objects.all()
    host_prefix = f"{request.scheme}://{request.get_host()}"
    
    context = {
        'form': form,
        'documents': documents,
        'host_prefix': host_prefix,
        'page_title': 'Document Uploader',
        'breadcrumb': 'Manage Documents',
    }
    return render(request, 'core/manage_documents.html', context)



