import os
import shutil
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_portal.settings')
django.setup()

from django.conf import settings
from core.models import Recognition, Achievement

def run():
    print("Starting import script...")
    
    # 1. Create target directories if they don't exist
    rec_media_dir = os.path.join(settings.MEDIA_ROOT, 'recognition')
    ach_media_dir = os.path.join(settings.MEDIA_ROOT, 'achievements')
    
    os.makedirs(rec_media_dir, exist_ok=True)
    os.makedirs(ach_media_dir, exist_ok=True)
    
    # Source directories
    rec_src_dir = r"C:\temp-csac\chaitanyafiles01.s3.amazonaws.com\chaitanyadoc"
    ach_src_dir = r"C:\temp-csac\chaitanyafiles01.s3.amazonaws.com\achievement"
    
    # 2. Copy recognition documents
    if os.path.exists(rec_src_dir):
        print(f"Copying files from {rec_src_dir} to {rec_media_dir}...")
        for filename in os.listdir(rec_src_dir):
            src_path = os.path.join(rec_src_dir, filename)
            if os.path.isfile(src_path):
                dest_path = os.path.join(rec_media_dir, filename)
                shutil.copy2(src_path, dest_path)
                print(f"Copied: {filename}")
    else:
        print(f"Source recognition directory not found: {rec_src_dir}")

    # 3. Copy achievement images
    if os.path.exists(ach_src_dir):
        print(f"Copying files from {ach_src_dir} to {ach_media_dir}...")
        for filename in os.listdir(ach_src_dir):
            src_path = os.path.join(ach_src_dir, filename)
            if os.path.isfile(src_path):
                dest_path = os.path.join(ach_media_dir, filename)
                shutil.copy2(src_path, dest_path)
                print(f"Copied: {filename}")
    else:
        print(f"Source achievement directory not found: {ach_src_dir}")

    # 4. Populate Recognition models
    recognitions_data = [
        ("UGC Autonomous Status Letter", "Autonomous-UGC.jpg", 1),
        ("CG Higher Education Department Letter", "HEI.jpg", 2),
        ("Functional MoUs and LoUs - Part I", "MoU1.jpg", 3),
        ("Functional MoUs and LoUs - Part II", "MoU2.jpg", 4),
        ("SNPV Autonomous Status Notification", "SNPV_Notification.jpg", 5),
        ("AICTE Approval Document", "aicte.png", 6),
        ("AISHE Recognition Document", "aishe-01.png", 7),
        ("IIC 3-Star Rating Certificate", "iic_3star.jpg", 8),
        ("Institution's Innovation Council Certificate", "iic-certificate.png", 9),
        ("NAAC Accreditation Certificate", "NAAC.jpeg", 10),
        ("SNPV University Approval Document", "SNPV-approval.png", 11),
        ("UGC University Recognition Document", "ugc-university.png", 12),
    ]

    for title, img_filename, order in recognitions_data:
        obj, created = Recognition.objects.get_or_create(
            title=title,
            defaults={
                'image': f'recognition/{img_filename}',
                'order': order
            }
        )
        if created:
            print(f"Created Recognition: {title}")
        else:
            # Update image to local and save
            obj.image = f'recognition/{img_filename}'
            obj.order = order
            obj.save()
            print(f"Updated Recognition: {title}")

    # 5. Populate Student Achievement models
    achievements_data = [
        ("Gold Medalists", "Our Gold Medalists", "recog1.png", 1),
        ("Sports Achievements", "Our Sports Achievements", "recog2.png", 2),
        ("Vibrant NSS", "Our Vibrant National Service Scheme Volunteers", "recog3.png", 3),
        ("Our Young Talents", "Our young and dynamic pool of talent", "recog4.png", 4),
    ]

    for title, description, img_filename, order in achievements_data:
        obj, created = Achievement.objects.get_or_create(
            title=title,
            defaults={
                'description': description,
                'image': f'achievements/{img_filename}',
                'order': order
            }
        )
        if created:
            print(f"Created Achievement: {title}")
        else:
            obj.description = description
            obj.image = f'achievements/{img_filename}'
            obj.order = order
            obj.save()
            print(f"Updated Achievement: {title}")

    print("Import script completed successfully!")

if __name__ == '__main__':
    run()
