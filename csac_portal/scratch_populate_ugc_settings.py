import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_portal.settings')
django.setup()

from core.models import UGCPageSettings, UGCGrant

def seed_ugc_settings():
    print("Seeding UGC Page Settings...")
    
    # 1. Seed or update UGCPageSettings
    settings, created = UGCPageSettings.objects.get_or_create(id=1)
    settings.heading = "University Grants Commission (UGC) Recognition"
    settings.description = (
        "Chaitanya Science and Arts College is recognized under Sections 2(f) and 12(B) of the UGC Act, 1956. "
        "This recognition establishes our credibility as a premier institution of higher learning eligible for "
        "central assistance and academic development programs. The college is committed to maintaining high "
        "standards of education, research, and infrastructure as mandated by the UGC."
    )
    settings.show_ugc_details = True
    settings.autonomy_status_title = "Autonomous"
    settings.autonomy_status_subtitle = "UGC Autonomous Status"
    settings.autonomy_status_text = "Empowered to design its own curriculum, conduct examinations, and evaluate student performance."
    
    settings.status_2f_12b_title = "2(f) and 12(B) Status"
    settings.status_2f_12b_text = (
        "The recognition under Section 2(f) signifies that our college is a recognized higher education institution.\n\n"
        "The Section 12(B) status makes the college eligible to receive developmental grants from the UGC and "
        "other central agencies for teaching, research, and infrastructure upgrades."
    )
    settings.benefits_title = "Autonomy Benefits"
    settings.benefits_list = (
        "Modernized, industry-relevant curriculum.\n"
        "Choice-Based Credit System (CBCS).\n"
        "Faster result processing and publication.\n"
        "Focus on skill-based and vocational courses."
    )
    settings.show_grants_section = True
    settings.grants_title = "UGC & Central Funding Support"
    settings.save()
    print(f"UGCPageSettings populated successfully (Created: {created})")

    # 2. Seed default UGC Grants
    grants_data = [
        {
            "scheme": "UGC Development Assistance",
            "purpose": "College Infrastructure & Lab Equipment",
            "impact": "Upgradation of Science labs and expansion of library resources.",
            "order": 1
        },
        {
            "scheme": "RUSA (Rashtriya Uchchatar Shiksha Abhiyan)",
            "purpose": "Institutional Restructuring & Quality Improvements",
            "impact": "Smart classrooms, campus-wide Wi-Fi, and digital library systems.",
            "order": 2
        },
        {
            "scheme": "UGC Minor/Major Projects",
            "purpose": "Faculty Research and Innovation Programs",
            "impact": "Financial support to faculty members for scientific and humanities research.",
            "order": 3
        }
    ]

    print("Seeding UGC Grants...")
    for idx, data in enumerate(grants_data):
        grant, g_created = UGCGrant.objects.get_or_create(
            scheme=data["scheme"],
            defaults={
                "purpose": data["purpose"],
                "impact": data["impact"],
                "order": data["order"],
                "is_active": True
            }
        )
        if not g_created:
            grant.purpose = data["purpose"]
            grant.impact = data["impact"]
            grant.order = data["order"]
            grant.save()
        print(f"Grant: '{grant.scheme}' (Created: {g_created})")
    
    print("Seeding completed successfully!")

if __name__ == "__main__":
    seed_ugc_settings()
