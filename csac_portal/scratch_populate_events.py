import os
import shutil
import django
from datetime import date

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_portal.settings')
django.setup()

from django.conf import settings
from core.models import Event

def run():
    print("Starting upcoming events populate script...")
    
    # Destination directories
    events_media_dir = os.path.join(settings.MEDIA_ROOT, 'events')
    brochures_media_dir = os.path.join(settings.MEDIA_ROOT, 'events', 'brochures')
    os.makedirs(events_media_dir, exist_ok=True)
    os.makedirs(brochures_media_dir, exist_ok=True)
    
    # Source directories for images and PDF brochures
    src_images_dir = r"C:\temp-csac\chaitanyafiles01.s3.amazonaws.com\eventImages"
    src_pdf_dir = os.path.join(settings.MEDIA_ROOT, 'policies')
    
    # Events definition
    events_data = [
        {
            "title": "National Conference on Innovations in Science & Technology (NCIST-2026)",
            "date": date(2026, 7, 15),
            "time": "10:00 AM",
            "location": "Seminar Hall, Science Block",
            "src_image": "1.jpg",
            "dest_image": "1.jpg",
            "description": "Chaitanya Science and Arts College is organizing the National Conference on Innovations in Science & Technology (NCIST-2026). The conference will bring together leading academicians, scientists, researchers, and students to exchange and share their experiences and research results on all aspects of Science, Arts, and technology. It also provides a premier interdisciplinary platform for researchers, practitioners, and educators to present and discuss the most recent innovations, trends, and concerns as well as practical challenges encountered and solutions adopted in the fields of Science & Technology.",
            "youtube_url": "https://www.youtube.com/watch?v=ScMzIvxBSi4",
            "registration_link": "https://docs.google.com/forms/d/e/1FAIpQLSfDmock_form_url_1/viewform",
            "pdf_src": "Green_Campus.pdf",
            "pdf_dest": "ncist_brochure.pdf",
            "link": ""
        },
        {
            "title": "Annual Cultural Fest & Talent Showcase 2026",
            "date": date(2026, 8, 22),
            "time": "05:00 PM",
            "location": "Open Air Theatre (OAT)",
            "src_image": "2.jpg",
            "dest_image": "2.jpg",
            "description": "Chaitanya Science and Arts College proudly announces its Annual Cultural Fest & Talent Showcase 2026. This mega-event is a celebration of student creativity, passion, and artistic brilliance. Events include Group Dance, Solo Singing, Theatre/Drama, Fine Arts, and Fashion Show. Prizes worth over Rs. 50,000 to be won. Join us in making this celebration unforgettable! All students from affiliated colleges are invited to register and participate.",
            "youtube_url": "https://www.youtube.com/watch?v=NTWhBrnVhfw",
            "registration_link": "https://docs.google.com/forms/d/e/1FAIpQLSfDmock_form_url_2/viewform",
            "pdf_src": "Environment_and_Energy_Conservation.pdf",
            "pdf_dest": "cultural_fest_brochure.pdf",
            "link": ""
        },
        {
            "title": "Workshop on Artificial Intelligence and Machine Learning Applications",
            "date": date(2026, 9, 10),
            "time": "11:00 AM",
            "location": "Central Computer Center",
            "src_image": "im4.jpg",
            "dest_image": "im4.jpg",
            "description": "Join our intensive 3-day workshop on Artificial Intelligence and Machine Learning Applications. Organized by the Department of Computer Science, this workshop will provide hands-on experience in training deep neural networks, implementing machine learning models using Python and PyTorch, and understanding natural language processing algorithms. Ideal for Computer Science, IT, and Mathematics students and researchers.",
            "youtube_url": "https://www.youtube.com/watch?v=NwbCZVm1exI",
            "registration_link": "https://docs.google.com/forms/d/e/1FAIpQLSfDmock_form_url_3/viewform",
            "pdf_src": "e-governance.pdf",
            "pdf_dest": "aiml_workshop_brochure.pdf",
            "link": ""
        },
        {
            "title": "Inter-College Sports Tournament & Athletic Meet",
            "date": date(2026, 10, 5),
            "time": "08:00 AM",
            "location": "College Play Grounds",
            "src_image": "j4.jpg",
            "dest_image": "j4.jpg",
            "description": "Gear up for the Chaitanya Annual Inter-College Sports Tournament & Athletic Meet. Sports events include Cricket, Football, Volleyball, Basketball, Badminton, and Athletic track events. Over 20 colleges from Chhattisgarh are participating. Food and accommodation will be provided to outstation teams. Registration is mandatory for team entries.",
            "youtube_url": "https://www.youtube.com/watch?v=ScMzIvxBSi4",
            "registration_link": "https://docs.google.com/forms/d/e/1FAIpQLSfDmock_form_url_4/viewform",
            "pdf_src": "Physically_Challenged_Students.pdf",
            "pdf_dest": "sports_meet_brochure.pdf",
            "link": ""
        }
    ]
    
    # Clear existing events
    Event.objects.all().delete()
    print("Cleared existing Event records.")
    
    seeded_count = 0
    for ed in events_data:
        # 1. Copy image file
        src_img_path = os.path.join(src_images_dir, ed["src_image"])
        dest_img_path = os.path.join(events_media_dir, ed["dest_image"])
        
        image_relative_path = None
        if os.path.exists(src_img_path):
            try:
                shutil.copy2(src_img_path, dest_img_path)
                image_relative_path = f"events/{ed['dest_image']}"
                print(f"Copied image {ed['src_image']} to media/events/{ed['dest_image']}")
            except Exception as e:
                print(f"Error copying image {ed['src_image']}: {e}")
        else:
            print(f"Warning: Source image not found at {src_img_path}")
            
        # 2. Copy PDF brochure file
        src_pdf_path = os.path.join(src_pdf_dir, ed["pdf_src"])
        dest_pdf_path = os.path.join(brochures_media_dir, ed["pdf_dest"])
        
        pdf_relative_path = None
        if os.path.exists(src_pdf_path):
            try:
                shutil.copy2(src_pdf_path, dest_pdf_path)
                pdf_relative_path = f"events/brochures/{ed['pdf_dest']}"
                print(f"Copied PDF {ed['pdf_src']} to media/events/brochures/{ed['pdf_dest']}")
            except Exception as e:
                print(f"Error copying PDF {ed['pdf_src']}: {e}")
        else:
            print(f"Warning: Source PDF not found at {src_pdf_path}")
            
        # 3. Create Event record
        event = Event(
            title=ed["title"],
            date=ed["date"],
            time=ed["time"],
            location=ed["location"],
            description=ed["description"],
            youtube_url=ed["youtube_url"],
            registration_link=ed["registration_link"],
            link=ed["link"],
            is_active=True
        )
        if image_relative_path:
            event.image = image_relative_path
        if pdf_relative_path:
            event.brochure = pdf_relative_path
        
        event.save()
        print(f"Seeded Event: '{ed['title']}' on {ed['date']}")
        seeded_count += 1
        
    print(f"Successfully seeded {seeded_count} events with full details!")

if __name__ == '__main__':
    run()
