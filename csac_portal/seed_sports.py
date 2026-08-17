import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_portal.settings')
django.setup()

from core.models import Notice, Event, Happening, SportsPageSettings, SportsGalleryImage
from django.utils import timezone

def seed_sports_data():
    print("Seeding sports page content...")

    # 1. Sports Page Settings (Singleton)
    settings_obj, created = SportsPageSettings.objects.get_or_create(pk=1)
    settings_obj.page_intro_title = "Sports & Athletics at CSAC"
    settings_obj.page_intro = (
        "Chaitanya Science and Arts College believes in the all-round development of its students. "
        "Physical education and sports form an integral part of our curriculum. The college boasts excellent "
        "sports infrastructure, specialized coaching programs, and modern fitness facilities that encourage "
        "students to participate and excel at regional, state, and national level competitions."
    )
    settings_obj.facilities = (
        "Outdoor Multi-purpose Sports Ground (Cricket, Football, Athletics Track)\n"
        "Indoor Sports Arena (Table Tennis, Chess, Carrom, Badminton Courts)\n"
        "Fully-equipped Fitness Center & Gymnasium\n"
        "State-of-the-art Volleyball & Basketball Courts\n"
        "First-Aid & Sports Rehabilitation Center"
    )
    settings_obj.achievements = (
        "Annual Athletic Meet - Inter-departmental track & field challenges with high participation\n"
        "Chaitanya Trophy Champions - Our team won the Inter-collegiate Volleyball Tournament 2025\n"
        "National Sports Day - Host of the region-wide sports and fitness awareness camp\n"
        "Yoga Day Celebrations - Annual mass yoga and wellness training for all students and faculty"
    )
    settings_obj.policies = (
        "Sports Quota Admissions for outstanding district, state, and national level players\n"
        "Cash incentives, fee concessions, and travel grants for tournament winners\n"
        "Special academic support, makeup exams, and attendance relief during tournament schedules\n"
        "Free specialized training and coaching under certified physical instructors"
    )
    settings_obj.show_notices = True
    settings_obj.show_events = True
    settings_obj.show_gallery = True
    settings_obj.show_happenings = True
    settings_obj.save()
    print("[-] SportsPageSettings seed updated.")

    # 2. Sports Gallery Images
    gallery_images = [
        {
            "image_url": "/media/gallery/images/sports01.png",
            "caption": "Students competing in the Annual Athletics Meet",
            "sport_tag": "Athletics",
            "order": 1
        },
        {
            "image_url": "/media/gallery/images/sports02.png",
            "caption": "CSAC Volleyball Team practicing on the college courts",
            "sport_tag": "Volleyball",
            "order": 2
        },
        {
            "image_url": "/media/gallery/images/sports03.png",
            "caption": "Intra-college Table Tennis singles final match",
            "sport_tag": "Table Tennis",
            "order": 3
        },
        {
            "image_url": "/media/happenings/national-sports-day.png",
            "caption": "Celebrating National Sports Day with students and coaches",
            "sport_tag": "Celebration",
            "order": 4
        }
    ]

    for img_data in gallery_images:
        img, created = SportsGalleryImage.objects.get_or_create(
            caption=img_data["caption"],
            defaults={
                "image_url": img_data["image_url"],
                "sport_tag": img_data["sport_tag"],
                "order": img_data["order"],
                "is_active": True
            }
        )
        if not created:
            img.image_url = img_data["image_url"]
            img.sport_tag = img_data["sport_tag"]
            img.order = img_data["order"]
            img.save()
    print(f"[-] Seeded {len(gallery_images)} SportsGalleryImage items.")

    # 3. Sports Notices
    notices = [
        {
            "title": "Selection Trials for CSAC Cricket & Volleyball Teams for Session 2026-27",
            "category": "sports",
            "published_date": timezone.now().date() - datetime.timedelta(days=2),
            "is_active": True
        },
        {
            "title": "Schedule for the upcoming Annual Athletic Meet & Track Events registration",
            "category": "sports",
            "published_date": timezone.now().date() - datetime.timedelta(days=5),
            "is_active": True
        },
        {
            "title": "Announcement of Cash Incentives and Scholarships for National/State Level Sports Winners",
            "category": "sports",
            "published_date": timezone.now().date() - datetime.timedelta(days=12),
            "is_active": True
        }
    ]

    for notice_data in notices:
        Notice.objects.get_or_create(
            title=notice_data["title"],
            defaults={
                "category": notice_data["category"],
                "published_date": notice_data["published_date"],
                "is_active": notice_data["is_active"]
            }
        )
    print(f"[-] Seeded {len(notices)} sports Notices.")

    # 4. Sports Events (Upcoming)
    # Check if event 8 exists and mark it as sports
    try:
        e8 = Event.objects.get(pk=8)
        e8.is_sports_event = True
        e8.save()
        print("[-] Updated existing Event ID 8 ('Inter-College Sports Tournament') to be a sports event.")
    except Event.DoesNotExist:
        Event.objects.create(
            pk=8,
            title="Inter-College Sports Tournament & Athletic Meet",
            date=timezone.now().date() + datetime.timedelta(days=15),
            time="09:00 AM",
            location="College Main Ground",
            is_sports_event=True,
            is_active=True,
            description="Join us for the grand inter-college athletics meet featuring track, volleyball, cricket and badminton events."
        )
        print("[-] Created Event ID 8 ('Inter-College Sports Tournament') as sports event.")

    # Additional upcoming events
    events = [
        {
            "title": "CSAC T-20 Cricket Trophy Finals",
            "date": timezone.now().date() + datetime.timedelta(days=25),
            "time": "10:00 AM",
            "location": "College Cricket Oval",
            "is_sports_event": True,
            "is_active": True,
            "description": "The final showdown of the inter-departmental T-20 cricket series. Come cheer for your department!"
        },
        {
            "title": "Selection Trials: State Level Badminton Tournament",
            "date": timezone.now().date() + datetime.timedelta(days=8),
            "time": "08:30 AM",
            "location": "Indoor Games Arena",
            "is_sports_event": True,
            "is_active": True,
            "description": "Trials for selecting CSAC single and double representatives for the state championship."
        }
    ]

    for ev_data in events:
        Event.objects.get_or_create(
            title=ev_data["title"],
            defaults={
                "date": ev_data["date"],
                "time": ev_data["time"],
                "location": ev_data["location"],
                "is_sports_event": ev_data["is_sports_event"],
                "is_active": ev_data["is_active"],
                "description": ev_data["description"]
            }
        )
    print(f"[-] Seeded {len(events)} upcoming sports Events.")

    # 5. Sports Happenings (Past Activities)
    happenings = [
        {
            "title": "National Sports Day Celebrated at CSAC with Enthusiasm and Fitness Run",
            "category": "Sports",
            "image_url": "/media/happenings/national-sports-day.png",
            "date": timezone.now().date() - datetime.timedelta(days=30),
            "is_sports_activity": True
        },
        {
            "title": "CSAC Volleyball Team Wins Inter-Collegiate Championship Trophy",
            "category": "Sports",
            "image_url": "/media/gallery/images/sports02.png",
            "date": timezone.now().date() - datetime.timedelta(days=45),
            "is_sports_activity": True
        },
        {
            "title": "Annual Athletic Meet 2025: Summary, Winners List, and Medal Tally",
            "category": "Sports",
            "image_url": "/media/gallery/images/sports01.png",
            "date": timezone.now().date() - datetime.timedelta(days=120),
            "is_sports_activity": True
        }
    ]

    for hap_data in happenings:
        # Check if already exists
        Happening.objects.get_or_create(
            title=hap_data["title"],
            defaults={
                "category": hap_data["category"],
                "image_url": hap_data["image_url"],
                "date": hap_data["date"],
                "is_sports_activity": hap_data["is_sports_activity"]
            }
        )
    print(f"[-] Seeded {len(happenings)} sports Happenings.")
    print("Done seeding sports data!")

if __name__ == '__main__':
    seed_sports_data()
