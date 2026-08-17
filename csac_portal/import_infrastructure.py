import os
import sys
import shutil
import django

# Configure Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "college_portal.settings")
django.setup()

from core.models import Infrastructure, InfrastructureImage

def main():
    source_dir = r"C:\infrastructure"
    
    # Define local folder db in workspace and django portal
    db_workspace = r"C:\temp-csac\chaitanyacg.ac.in\db"
    db_portal = r"C:\temp-csac\csac_portal\db"
    media_infra_dir = r"C:\temp-csac\csac_portal\media\infrastructure"

    # Create directories if they do not exist
    os.makedirs(db_workspace, exist_ok=True)
    os.makedirs(db_portal, exist_ok=True)
    os.makedirs(media_infra_dir, exist_ok=True)

    print("Copying files to local folder db and media folder...")
    
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
        # Copy to media/infrastructure folder
        shutil.copy2(src_path, os.path.join(media_infra_dir, filename))
            
    print(f"Copied {len(files)} files successfully.")

    # Clear existing data to prevent duplicates and start clean
    print("Clearing existing infrastructure data...")
    InfrastructureImage.objects.all().delete()
    Infrastructure.objects.all().delete()

    # Define the infrastructure data structure
    infra_data = [
        {
            "title": "Scientific Laboratories",
            "description": "Our state-of-the-art laboratories are fully equipped with advanced modern instruments to cater to both undergraduate and postgraduate course requirements. Each lab is properly ventilated, spacious, and designed with optimal safety features, allowing students to conduct research, experiments, and practical studies under expert mentorship. Specializations include Chemistry, Physics, Botany, Zoology, and Forestry.",
            "video_url": "https://www.youtube.com/watch?v=NwbCZVm1exI",
            "order": 1,
            "images": [
                {"filename": "GMC10032024_160324.jpg", "caption": "Chemistry Laboratory"},
                {"filename": "GMC29052024_112856.jpg", "caption": "Physics Laboratory"},
                {"filename": "GMC29052024_121539.jpg", "caption": "Botany Laboratory"},
                {"filename": "IMG_20241115_111109160_AE.jpg", "caption": "Zoology Laboratory"},
                {"filename": "IMG_20241115_111149846_HDR_AE.jpg", "caption": "Forestry Laboratory"},
                {"filename": "IMG_20241115_111425001_AE.jpg", "caption": "Research Instrumentation Center"}
            ]
        },
        {
            "title": "Central Digital Library",
            "description": "The Central Library serves as the academic heart of the institution, housing a comprehensive collection of over 15,000 reference books, journals, textbooks, and encyclopedias. Equipped with high-speed internet connectivity, the digital section provides students and faculty with seamless access to premium databases and resources, including INFLIBNET, SWAYAM, e-Pathshala, MOOCs, and the National Digital Library (NDL).",
            "video_url": "",
            "order": 2,
            "images": [
                {"filename": "Lib1.jpeg", "caption": "Main Library Reading Hall"},
                {"filename": "WhatsApp_Image_2025-01-02_at_10.53.56_AM.jpeg", "caption": "Digital Library Section"},
                {"filename": "WhatsApp_Image_2025-01-02_at_11.01.39_AM.jpeg", "caption": "Book Stacks and Reference Section"}
            ]
        },
        {
            "title": "Advanced Computer Center",
            "description": "Our advanced Computer Center is designed to support the growing digital needs of all academic streams. Equipped with the latest workstations, enterprise-grade software, and high-speed Wi-Fi, the lab provides an ideal environment for programming, database management, web development, and digital literacy. Regular workshops on emerging tech (Python, Web Tech) are conducted here.",
            "video_url": "",
            "order": 3,
            "images": [
                {"filename": "WhatsApp_Image_2024-11-13_at_11.17.58_AM_1.jpeg", "caption": "Main Computer Lab"}
            ]
        },
        {
            "title": "Smart & Interactive Classrooms",
            "description": "Modern air-conditioned classrooms equipped with interactive smart boards, LCD projectors, and sound systems to facilitate ICT-enabled active learning. These spaces foster collaborative learning, group discussions, and high-quality multimedia presentations.",
            "video_url": "",
            "order": 4,
            "images": [
                {"filename": "Smart_Class.jpg", "caption": "Smart Classroom"},
                {"filename": "Interactive_Class.jpg", "caption": "Interactive Learning Center"}
            ]
        },
        {
            "title": "Gramvithika (Rural Heritage Center)",
            "description": "A unique campus museum showcasing the rich rural heritage, traditional artifacts, folk arts, and culture of Chhattisgarh. Gramvithika serves as an experiential learning gallery for humanities students and visitors alike, promoting local arts and traditions.",
            "video_url": "",
            "order": 5,
            "images": [
                {"filename": "gramvithika.jpg", "caption": "Gramvithika Heritage Gallery"}
            ]
        },
        {
            "title": "Cultural & Music Center",
            "description": "Equipped with traditional and modern musical instruments, the Music Center provides a creative space for students interested in vocal and instrumental music, dance, and theater. Regular training sessions and cultural events are organized to nurture talent.",
            "video_url": "",
            "order": 6,
            "images": [
                {"filename": "musiccenter.jpg", "caption": "Music Training Hall"}
            ]
        },
        {
            "title": "Lush Green Eco-Campus",
            "description": "The college boasts a clean, green, and sustainable eco-campus featuring lush botanical gardens, a medicinal herbal garden with over 150 species of plants, and tree-lined pathways. The serene environment provides a natural setting conducive to learning and well-being.",
            "video_url": "",
            "order": 7,
            "images": [
                {"filename": "IMG_20241115_112537854_AE.jpg", "caption": "College Main Garden"},
                {"filename": "IMG_20241115_112642364_HDR_AE.jpg", "caption": "Medicinal Herbal Garden"},
                {"filename": "IMG_20241115_113202798_HDR_AE.jpg", "caption": "Eco Path & Green Canopy"},
                {"filename": "IMG_20241115_113337902_HDR_AE.jpg", "caption": "Botanical Showcase Area"},
                {"filename": "IMG_20241115_113514956_HDR_AE.jpg", "caption": "Central Lawn"},
                {"filename": "IMG_20241115_113659084_HDR_AE.jpg", "caption": "Campus Flora Study Zone"},
                {"filename": "IMG_20241115_114023148_HDR_AE.jpg", "caption": "Green Campus Vista"},
                {"filename": "IMG_20241115_114119571_HDR_AE.jpg", "caption": "Serene Student Sit-out area"}
            ]
        }
    ]

    # Insert data into the database
    for idx, item in enumerate(infra_data):
        infra_obj = Infrastructure.objects.create(
            title=item["title"],
            description=item["description"],
            video_url=item["video_url"],
            order=item["order"]
        )
        print(f"Created Infrastructure section: {infra_obj.title}")
        
        for img_idx, img_info in enumerate(item["images"]):
            # Set the image field using relative path in the media directory
            img_rel_path = f"infrastructure/{img_info['filename']}"
            InfrastructureImage.objects.create(
                infrastructure=infra_obj,
                image=img_rel_path,
                caption=img_info["caption"],
                order=img_idx + 1
            )
            print(f"  Added image: {img_info['filename']} - {img_info['caption']}")

    print("Data successfully seeded into database.")

if __name__ == "__main__":
    main()
