import os
import sys
import shutil
import django

# Configure Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "college_portal.settings")
django.setup()

from core.models import BannerSlide

def main():
    source_dir = r"C:\slider"
    
    # Define local folder db in workspace and django portal
    db_workspace = r"C:\temp-csac\chaitanyacg.ac.in\db"
    db_portal = r"C:\temp-csac\csac_portal\db"
    media_banner_dir = r"C:\temp-csac\csac_portal\media\banner"

    # Create directories if they do not exist
    os.makedirs(db_workspace, exist_ok=True)
    os.makedirs(db_portal, exist_ok=True)
    os.makedirs(media_banner_dir, exist_ok=True)

    print("Copying files to local folder db and media banner folder...")
    
    if not os.path.exists(source_dir):
        print(f"Error: Source directory {source_dir} does not exist.")
        return

    files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
    
    for filename in files:
        src_path = os.path.join(source_dir, filename)
        
        # Copy to workspace db
        shutil.copy2(src_path, os.path.join(db_workspace, filename))
        # Copy to portal db
        shutil.copy2(src_path, os.path.join(db_portal, filename))
        # Copy to media/banner folder
        shutil.copy2(src_path, os.path.join(media_banner_dir, filename))
            
    print(f"Copied {len(files)} files successfully.")

    # Clear existing slides
    print("Clearing existing banner slides...")
    BannerSlide.objects.all().delete()

    # Define new slides
    slides_data = [
        {
            "filename": "20250102_162201.jpg",
            "caption": "Chaitanya Science & Arts College Campus",
            "order": 1
        },
        {
            "filename": "Conferencec Hall.jpg",
            "caption": "State-of-the-Art Conference Hall",
            "order": 2
        },
        {
            "filename": "Cultural Programs.JPG",
            "caption": "Vibrant Cultural Programs & Extracurricular Activities",
            "order": 3
        },
        {
            "filename": "Enriched Library.jpg",
            "caption": "Enriched Library & Digital Resource Access Center",
            "order": 4
        },
        {
            "filename": "Garden.png",
            "caption": "Lush Green Campus & Eco-Gardens",
            "order": 5
        },
        {
            "filename": "Music Center.jpg",
            "caption": "Music & Performing Arts Center",
            "order": 6
        },
        {
            "filename": "Prayer.png",
            "caption": "Daily College Assembly and Traditional Morning Prayer",
            "order": 7
        },
        {
            "filename": "Seceratory Higher Education, Raipur C.G..png",
            "caption": "Visit of Secretary, Department of Higher Education, Raipur (C.G.)",
            "order": 8
        }
    ]

    for slide in slides_data:
        image_rel_path = f"banner/{slide['filename']}"
        BannerSlide.objects.create(
            caption=slide["caption"],
            image=image_rel_path,
            image_url="",
            order=slide["order"],
            is_active=True
        )
        print(f"Created BannerSlide: {slide['caption']} ({slide['filename']})")

    print("Banner slides successfully populated in database.")

if __name__ == "__main__":
    main()
