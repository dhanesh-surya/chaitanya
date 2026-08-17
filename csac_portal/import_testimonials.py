import os
import shutil
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_portal.settings')
django.setup()

from core.models import Testimonial

def import_testimonials():
    src_dir = r"C:\chaitanyafiles01.s3.amazonaws.com\testimonials"
    dst_dir = os.path.join("media", "testimonials")
    
    # Create destination directory if not exists
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
        print(f"Created directory: {dst_dir}")
        
    testimonials_data = [
        {
            "student_name": "Rani Gauraha",
            "program": "M.Sc. Zoology (2022-23)",
            "rating": 5,
            "text": "My M.Sc. in Zoology was exceptional, offering in-depth learning, fieldwork experience, and outstanding mentorship. Truly a life-changing journey!",
            "filename": "IMG-20240726-WA0010.jpg",
            "order": 1
        },
        {
            "student_name": "Nidhi Devdas",
            "program": "B.Sc. Bio (2022-23)",
            "rating": 5,
            "text": "Completing my B.Sc in Biology was transformative, providing hands-on experience, deep knowledge, and inspiring a passion for research. Highly recommended!",
            "filename": "IMG-20240726-WA0011.jpg",
            "order": 2
        },
        {
            "student_name": "Jharna Sahu",
            "program": "MSW (2022-23)",
            "rating": 5,
            "text": "The supportive faculty and dynamic learning environment helped me build confidence and expertise in social work practice.",
            "filename": "Jharna_MSW.jpg",
            "order": 3
        },
        {
            "student_name": "Bhawna Kashyap",
            "program": "M.Sc. Botany (2022-23)",
            "rating": 5,
            "text": "M.Sc. Botany at this college provided excellent academic guidance, practical exposure, and research opportunities for my career development.",
            "filename": "Bhawana_Kashyap_Bot_2nd.jpeg",
            "order": 4
        },
        {
            "student_name": "Manisha Kurrey",
            "program": "M.A. SOCIOLOGY",
            "rating": 5,
            "text": "M.A. Sociology helped me critically explore social structures, inequalities, and human behavior. Highly recommended for future sociologists.",
            "filename": "Manisha_Kurrey_BA.jpg",
            "order": 5
        }
    ]
    
    for item in testimonials_data:
        src_path = os.path.join(src_dir, item["filename"])
        dst_path = os.path.join(dst_dir, item["filename"])
        
        # Copy image file to local testimonials media directory
        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path)
            print(f"Copied {item['filename']} to {dst_path}")
        else:
            print(f"Warning: Source image {src_path} not found!")
            
        # Get or create testimonial record in the database
        photo_field_value = f"testimonials/{item['filename']}"
        t, created = Testimonial.objects.get_or_create(
            student_name=item["student_name"],
            defaults={
                "program": item["program"],
                "rating": item["rating"],
                "text": item["text"],
                "photo": photo_field_value,
                "order": item["order"]
            }
        )
        if not created:
            t.program = item["program"]
            t.rating = item["rating"]
            t.text = item["text"]
            t.photo = photo_field_value
            t.order = item["order"]
            t.save()
            print(f"Updated Testimonial for {item['student_name']}")
        else:
            print(f"Created Testimonial for {item['student_name']}")

if __name__ == '__main__':
    import_testimonials()
