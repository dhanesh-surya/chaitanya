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
    source_new_dir = r"C:\slider"
    source_old_dir = r"C:\chaitanyafiles01.s3.amazonaws.com\homeImages"
    
    # Define local folder db in workspace and django portal
    db_workspace = r"C:\temp-csac\chaitanyacg.ac.in\db"
    db_portal = r"C:\temp-csac\csac_portal\db"
    media_banner_dir = r"C:\temp-csac\csac_portal\media\banner"

    # Create directories if they do not exist
    os.makedirs(db_workspace, exist_ok=True)
    os.makedirs(db_portal, exist_ok=True)
    os.makedirs(media_banner_dir, exist_ok=True)

    # Copy new slider images
    print("Copying new slider files...")
    if os.path.exists(source_new_dir):
        new_files = [f for f in os.listdir(source_new_dir) if os.path.isfile(os.path.join(source_new_dir, f))]
        for filename in new_files:
            src_path = os.path.join(source_new_dir, filename)
            shutil.copy2(src_path, os.path.join(db_workspace, filename))
            shutil.copy2(src_path, os.path.join(db_portal, filename))
            shutil.copy2(src_path, os.path.join(media_banner_dir, filename))
        print(f"Copied {len(new_files)} new files.")
    else:
        print(f"Error: New slider source directory {source_new_dir} does not exist.")

    # Copy old slider images
    print("Copying old slider files...")
    if os.path.exists(source_old_dir):
        old_files = [f for f in os.listdir(source_old_dir) if os.path.isfile(os.path.join(source_old_dir, f))]
        for filename in old_files:
            src_path = os.path.join(source_old_dir, filename)
            shutil.copy2(src_path, os.path.join(db_workspace, filename))
            shutil.copy2(src_path, os.path.join(db_portal, filename))
            shutil.copy2(src_path, os.path.join(media_banner_dir, filename))
        print(f"Copied {len(old_files)} old files.")
    else:
        print(f"Error: Old slider source directory {source_old_dir} does not exist.")

    # Clear existing slides in DB
    print("Clearing existing banner slides from DB...")
    BannerSlide.objects.all().delete()

    # Define new slides (order 1 to 8)
    new_slides_data = [
        {"filename": "20250102_162201.jpg", "caption": "Chaitanya Science & Arts College Campus"},
        {"filename": "Conferencec Hall.jpg", "caption": "State-of-the-Art Conference Hall"},
        {"filename": "Cultural Programs.JPG", "caption": "Vibrant Cultural Programs & Extracurricular Activities"},
        {"filename": "Enriched Library.jpg", "caption": "Enriched Library & Digital Resource Access Center"},
        {"filename": "Garden.png", "caption": "Lush Green Campus & Eco-Gardens"},
        {"filename": "Music Center.jpg", "caption": "Music & Performing Arts Center"},
        {"filename": "Prayer.png", "caption": "Daily College Assembly and Traditional Morning Prayer"},
        {"filename": "Seceratory Higher Education, Raipur C.G..png", "caption": "Visit of Secretary, Department of Higher Education, Raipur (C.G.)"}
    ]

    # Define old slides (order 9 to 35)
    # Matching captions with exact HTML structure
    old_slides_data = [
        {"filename": "25%E0%A4%B5_%E0%A4%B0%E0%A4%9C%E0%A4%A4_%E0%A4%9C%E0%A4%AF%E0%A4%A4_2.jpg", "caption": "25 Year of Excellence"},
        {"filename": "CHAITANYA_SCIENCE_AND_ARTS_COLLEGE_1.png", "caption": "NAAC GRADE A AWARD"},
        {"filename": "3_Star_Rating_IIC.png", "caption": "3 Star Rating IIC"},
        {"filename": "pic9.jpg", "caption": "दक्षिण मध्य क्षेत्र सांस्कृतिक केन्द्र, संस्कृति मंत्रालय, भारत सरकार की प्रस्तुति महाविद्यालय परिसर में."},
        {"filename": "SS02.jpg", "caption": "श्री एसएस बजाज सर ने संस्थागत नवाचार परिषद (IIC)का निरीक्षण किया।"},
        {"filename": "Global-Awards.jpg", "caption": "The Progress Global Awards 2024 under Best Social and Community Services"},
        {"filename": "dr_kiran_seth.png", "caption": "पद्मश्री डॉ. किरण सेठ,संस्थापक- स्पिक मैके"},
        {"filename": "pic10.jpg", "caption": "प्राध्यापकगण एवं छात्र-छात्राएं"},
        {"filename": "pic7.jpg", "caption": "डॉ. चितरंजन कर , भाषाविद एवं पूर्व अध्यक्ष, साहित्य एवं भाषा अध्ययन शाला, पं. रविशंकर शुक्ल विश्वविद्यालय, रायपुर (छ.ग.) (छत्तीसगढ़ी भाषा और लोक साहित्य कार्यशाला ) के अवसर पर"},
        {"filename": "College_Building.png", "caption": "college building"},
        {"filename": "Padmashri_Damodar_Ganesh_Bapat_.jpg", "caption": "पद्मश्री दामोदर गणेश बापट जी"},
        {"filename": "Capt_Y_Sriniwas.jpg", "caption": "Grp Capt. Y Srinivas, RMOC, Atal Innovation Mission Niti Aayog, Delhi"},
        {"filename": "pic6.jpg", "caption": ".."},
        {"filename": "pic3.jpg", "caption": "."},
        {"filename": "pic8.jpg", "caption": "."},
        {"filename": "Bhart-Bandhu.jpg", "caption": "पद्मश्री भारती बंधू  महाविद्यालय परिसर में"},
        {"filename": "Janjgir-Mela.jpg", "caption": "जाज्वल्यदेव लोक महोत्सव एवं एग्रीटेक कृषि मेला 2024"},
        {"filename": "VC_GD_Sharma.png", "caption": "प्रो.जी.डी.शर्मा, अध्यक्ष, भारतीय विश्वविद्यालय संघ"},
        {"filename": "Merit_List.png", "caption": "गोल्ड मैडल प्राप्त छात्र - छात्राएं"},
        {"filename": "4.png", "caption": "पद्मश्री डॉ. सुरेन्द्र दुबे, चैतन्य महोत्सव 2020"},
        {"filename": "VC_LP_SNPV.png", "caption": "प्रो. (डॉ.) ललित प्रकाश पटेरिया,माननीय कुलपति, शहीद नंदकुमार पटेल विश्वविद्यालय, रायगढ़"},
        {"filename": "pic11.jpg", "caption": "प्रो. (डॉ.) ललित प्रकाश पटेरिया,माननीय कुलपति, शहीद नंदकुमार पटेल विश्वविद्यालय, रायगढ़ - विश्व पर्यावरण दिवस के अवसर पर महाविद्यालय परिसर में"},
        {"filename": "Author_Kent_Dickerson_1.jpg", "caption": "अमेरिकी  लेखक केंट डीकर्सन महाविद्यालय परिसर में"},
        {"filename": "SS03.jpg", "caption": "श्री एस.एस. बजाज, राष्ट्रीय विज्ञान दिवस 2024 के आयोजन में मुख्य अतिथि के रूप में शामिल हुए"},
        {"filename": "Bajaj-Sir.jpg", "caption": "श्री एस.एस. बजाज,महानिदेशक, छत्तीसगढ़ विज्ञान एवं प्रौद्योगिकी परिषद - राष्ट्रीय विज्ञान दिवस 2024 के अवसर पर विज्ञान प्रदर्शनी में"},
        {"filename": "Shri_Anuj_Sharma.png", "caption": "पद्मश्री अनुज शर्मा"},
        {"filename": "vcnewsnpv.jpg", "caption": "शहीद नंदकुमार पटेल विश्वविद्यालय, रायगढ़ के नवनियुक्त माननीय कुलपति,  प्रो. विनय चौहान से महाविद्यालय के संचालक श्री वीरेन्द्र तिवारी की सौजन्य मुलाकात"}
    ]

    current_order = 1
    
    # Insert new slides
    for slide in new_slides_data:
        image_rel_path = f"banner/{slide['filename']}"
        BannerSlide.objects.create(
            caption=slide["caption"],
            image=image_rel_path,
            image_url="",
            order=current_order,
            is_active=True
        )
        print(f"Created New Slide (Order {current_order}): {slide['filename']}")
        current_order += 1

    # Insert old slides
    for slide in old_slides_data:
        image_rel_path = f"banner/{slide['filename']}"
        BannerSlide.objects.create(
            caption=slide["caption"],
            image=image_rel_path,
            image_url="",
            order=current_order,
            is_active=True
        )
        print(f"Created Old Slide (Order {current_order}): {slide['filename']}")
        current_order += 1

    print(f"All {current_order - 1} banner slides populated successfully.")

if __name__ == "__main__":
    main()
