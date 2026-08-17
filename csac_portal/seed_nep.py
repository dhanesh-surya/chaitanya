import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_portal.settings')
django.setup()

from core.models import NEPTab, NEPTabFile, NEPTabLink

def seed_nep_data():
    print("Seeding NEP Tab data...")
    
    # Tab 1: NEP 2020 Overview
    t1, created = NEPTab.objects.get_or_create(
        title="NEP 2020 Overview",
        defaults={
            "description": (
                "<p>Chaitanya Science and Arts College has adopted the National Education Policy (NEP) 2020 framework "
                "to transition towards a more holistic, flexible, and multidisciplinary system of higher education. "
                "NEP 2020 aims to empower students by giving them choice and flexibility, focusing on skill development, "
                "and fostering research at all levels.</p>"
            ),
            "order": 1,
            "is_active": True
        }
    )
    if not created:
        t1.description = (
            "<p>Chaitanya Science and Arts College has adopted the National Education Policy (NEP) 2020 framework "
            "to transition towards a more holistic, flexible, and multidisciplinary system of higher education. "
            "NEP 2020 aims to empower students by giving them choice and flexibility, focusing on skill development, "
            "and fostering research at all levels.</p>"
        )
        t1.order = 1
        t1.save()
        print("Updated Overview Tab.")
    else:
        print("Created Overview Tab.")
        
    # Link for Tab 1
    NEPTabLink.objects.get_or_create(
        tab=t1,
        url="https://www.education.gov.in/nep-2020",
        defaults={
            "title": "Ministry of Education - NEP 2020 Portal",
            "order": 1
        }
    )
    
    # Tab 2: UG Program Structure
    t2, created = NEPTab.objects.get_or_create(
        title="UG Program Structure",
        defaults={
            "description": (
                "<p>The undergraduate curriculum under NEP 2020 offers multiple entry and exit choices:</p>"
                "<ul>"
                "<li><strong>Exit after Year 1:</strong> UG Certificate (40 - 44 Credits required)</li>"
                "<li><strong>Exit after Year 2:</strong> UG Diploma (80 - 88 Credits required)</li>"
                "<li><strong>Exit after Year 3:</strong> Bachelor's Degree (120 - 132 Credits required)</li>"
                "<li><strong>Complete Year 4:</strong> Bachelor's Degree (Honors / with Research) (160 - 176 Credits required)</li>"
                "</ul>"
            ),
            "order": 2,
            "is_active": True
        }
    )
    if not created:
        t2.description = (
            "<p>The undergraduate curriculum under NEP 2020 offers multiple entry and exit choices:</p>"
            "<ul>"
            "<li><strong>Exit after Year 1:</strong> UG Certificate (40 - 44 Credits required)</li>"
            "<li><strong>Exit after Year 2:</strong> UG Diploma (80 - 88 Credits required)</li>"
            "<li><strong>Exit after Year 3:</strong> Bachelor's Degree (120 - 132 Credits required)</li>"
            "<li><strong>Complete Year 4:</strong> Bachelor's Degree (Honors / with Research) (160 - 176 Credits required)</li>"
            "</ul>"
        )
        t2.order = 2
        t2.save()
        print("Updated UG Program Structure Tab.")
    else:
        print("Created UG Program Structure Tab.")

    # Tab 3: ABC & DigiLocker Integration
    t3, created = NEPTab.objects.get_or_create(
        title="ABC & DigiLocker Integration",
        defaults={
            "description": (
                "<p><strong>Academic Bank of Credits (ABC)</strong> is a digital repository that securely stores "
                "academic credits earned by students. Students must register on the ABC portal to get their unique ABC ID, "
                "which is mandatory for semester exams and credit transfers.</p>"
            ),
            "order": 3,
            "is_active": True
        }
    )
    if not created:
        t3.description = (
            "<p><strong>Academic Bank of Credits (ABC)</strong> is a digital repository that securely stores "
            "academic credits earned by students. Students must register on the ABC portal to get their unique ABC ID, "
            "which is mandatory for semester exams and credit transfers.</p>"
        )
        t3.order = 3
        t3.save()
        print("Updated ABC Tab.")
    else:
        print("Created ABC Tab.")
        
    # Links for Tab 3
    NEPTabLink.objects.get_or_create(
        tab=t3,
        url="https://www.abc.gov.in/",
        defaults={
            "title": "Register on ABC (Academic Bank of Credits) Portal",
            "order": 1
        }
    )
    NEPTabLink.objects.get_or_create(
        tab=t3,
        url="https://www.digilocker.gov.in/",
        defaults={
            "title": "Access DigiLocker Services",
            "order": 2
        }
    )
    
    print("Seeding finished successfully!")

if __name__ == '__main__':
    seed_nep_data()
