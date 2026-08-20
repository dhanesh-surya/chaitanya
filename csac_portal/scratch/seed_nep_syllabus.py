import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_portal.settings')
django.setup()

from academics.models import Department, Syllabus

nep_syllabus_data = [
    # Bachelor of Arts
    {"title": "BA NEP English Literature Syllabus", "dept": "English", "url": "https://snpv.ac.in/storage/notification/snpv-1785497637.pdf"},
    {"title": "BA NEP History Syllabus", "dept": "History", "url": "https://snpv.ac.in/storage/notification/snpv-1785497607.pdf"},
    {"title": "BA NEP Economics Syllabus", "dept": "Economics", "url": "https://snpv.ac.in/storage/notification/snpv-1785497578.pdf"},
    {"title": "BA NEP Political Science Syllabus", "dept": "Political Science", "url": "https://snpv.ac.in/storage/notification/snpv-1785497509.pdf"},
    {"title": "BA NEP Sanskrit Syllabus", "dept": "Hindi", "url": "https://snpv.ac.in/storage/notification/snpv-1785497477.pdf"},
    {"title": "BA NEP Music Syllabus", "dept": "Music", "url": "https://snpv.ac.in/storage/notification/snpv-1785497457.pdf"},
    {"title": "BA NEP Sociology Syllabus", "dept": "Sociology", "url": "https://snpv.ac.in/storage/notification/snpv-1785497430.pdf"},
    {"title": "BA NEP Public Administration Syllabus", "dept": "Political Science", "url": "https://snpv.ac.in/storage/notification/snpv-1785497410.pdf"},
    {"title": "BA NEP Hindi Literature Syllabus", "dept": "Hindi", "url": "https://snpv.ac.in/storage/notification/snpv-1785497263.pdf"},
    {"title": "BA NEP Geography Syllabus", "dept": "Geography", "url": "https://snpv.ac.in/storage/notification/snpv-1785497237.pdf"},
    {"title": "BA NEP Psychology Syllabus", "dept": "Sociology", "url": "https://snpv.ac.in/storage/notification/snpv-1785497161.pdf"},
    {"title": "BA NEP Philosophy Syllabus", "dept": "Hindi", "url": "https://snpv.ac.in/storage/notification/snpv-1785497694.pdf"},

    # Bachelor of Science
    {"title": "BSc NEP Mathematics Syllabus", "dept": "Mathematics", "url": "https://snpv.ac.in/storage/notification/snpv-1785498169.pdf"},
    {"title": "BSc NEP Chemistry Syllabus", "dept": "Chemistry", "url": "https://snpv.ac.in/storage/notification/snpv-1785498150.pdf"},
    {"title": "BSc NEP Physics Syllabus", "dept": "Physics", "url": "https://snpv.ac.in/storage/notification/snpv-1785498112.pdf"},
    {"title": "BSc NEP Biotechnology Syllabus", "dept": "Zoology", "url": "https://snpv.ac.in/storage/notification/snpv-1785498091.pdf"},
    {"title": "BSc NEP Microbiology Syllabus", "dept": "Botany", "url": "https://snpv.ac.in/storage/notification/snpv-1785498063.pdf"},
    {"title": "BSc NEP Computer Science Syllabus", "dept": "Computer Science", "url": "https://snpv.ac.in/storage/notification/snpv-1785498043.pdf"},
    {"title": "BSc NEP Information Technology Syllabus", "dept": "Computer Science", "url": "https://snpv.ac.in/storage/notification/snpv-1785497980.pdf"},
    {"title": "BSc NEP Zoology Syllabus", "dept": "Zoology", "url": "https://snpv.ac.in/storage/notification/snpv-1785497959.pdf"},
    {"title": "BSc NEP Botany Syllabus", "dept": "Botany", "url": "https://snpv.ac.in/storage/notification/snpv-1785497932.pdf"},
    {"title": "BSc NEP Forestry and Wildlife Syllabus", "dept": "Forestry and Wildlife", "url": "https://snpv.ac.in/storage/notification/snpv-1785497897.pdf"},
    {"title": "BSc NEP Home Science Syllabus", "dept": "Sociology", "url": "https://snpv.ac.in/storage/notification/snpv-1785499713.pdf"},
    {"title": "BSc NEP Bio Chemistry Syllabus", "dept": "Chemistry", "url": "https://snpv.ac.in/storage/notification/snpv-1785499781.pdf"},

    # Bachelor of Commerce
    {"title": "BCom NEP Syllabus", "dept": "Commerce & Management", "url": "https://snpv.ac.in/storage/notification/snpv-1755169717.pdf"},

    # Bachelor of Business Administration
    {"title": "BBA NEP Syllabus", "dept": "Commerce & Management", "url": "https://snpv.ac.in/storage/notification/snpv-1785499514.pdf"},

    # Bachelor of Art Home Science
    {"title": "BA NEP Home Science Syllabus", "dept": "Sociology", "url": "https://snpv.ac.in/storage/notification/snpv-1785498632.pdf"},

    # Bachelor of Computer Application
    {"title": "BCA NEP Computer Application Syllabus", "dept": "Computer Science", "url": "https://snpv.ac.in/storage/notification/snpv-1785498802.pdf"},
]

def seed_syllabi():
    created_count = 0
    updated_count = 0

    for item in nep_syllabus_data:
        try:
            department = Department.objects.get(name=item['dept'])
        except Department.DoesNotExist:
            print(f"Warning: Department '{item['dept']}' not found in database. Skipping '{item['title']}'.")
            continue

        # Get or create the syllabus record
        syllabus, created = Syllabus.objects.get_or_create(
            title=item['title'],
            defaults={
                'department': department,
                'document_url': item['url'],
                'academic_year': '2025-26',
                'is_nep_2020': True
            }
        )

        if created:
            created_count += 1
        else:
            # Update the URL and field just in case
            syllabus.document_url = item['url']
            syllabus.is_nep_2020 = True
            syllabus.save()
            updated_count += 1

    print(f"Completed! Created {created_count} new entries, updated {updated_count} existing entries.")

if __name__ == '__main__':
    seed_syllabi()
