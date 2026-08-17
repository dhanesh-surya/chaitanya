import os
import sys
import shutil
import django

# Add current working directory to sys.path
sys.path.insert(0, os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_portal.settings')
django.setup()

from core.models import LibraryPageSettings, LibraryBookCategory, LibraryResource, LibraryGalleryImage

def seed_library():
    print("Seeding Library Page Settings...")
    # Clean existing
    LibraryPageSettings.objects.all().delete()
    LibraryBookCategory.objects.all().delete()
    LibraryResource.objects.all().delete()
    LibraryGalleryImage.objects.all().delete()

    # Create local media folders for library
    media_library_dir = os.path.join('media', 'library')
    media_gallery_dir = os.path.join('media', 'library', 'gallery')
    os.makedirs(media_library_dir, exist_ok=True)
    os.makedirs(media_gallery_dir, exist_ok=True)

    # Source image path
    src_image = os.path.join('..', 'chaitanyacg.ac.in', 'static', 'assets', 'images', 'feature', '0001.png')
    dest_image_rel = 'library/0001.png'
    dest_image_full = os.path.join('media', dest_image_rel)

    copied = False
    if os.path.exists(src_image):
        try:
            shutil.copy(src_image, dest_image_full)
            print(f"Successfully copied library image to {dest_image_full}")
            copied = True
        except Exception as e:
            print(f"Error copying library image: {e}")
    else:
        print(f"Source image not found at {src_image}. Fallback path will be used.")

    # Create Settings
    settings = LibraryPageSettings.objects.create(
        page_intro_title="Learning Resources of the College: Smt. Urmila Devi Smriti Pustkaalaya",
        page_intro="Discover the heart of academic exploration at the College Library, established in 2001 in loving memory of Smt. Urmila Devi. More than just a repository of knowledge, our library is a dynamic hub that caters to the diverse needs of both faculty and students.",
        about_library_title="About The Library",
        about_library_text="With a spacious environment welcoming up to 100 readers, we offer semi-automated services and house an impressive collection of 2000 physical books and research journals. Access to digital subscriptions such as INFIBNET and open-access journals enriches research opportunities. With RFID technology ensuring seamless operations, our library hosts a variety of engaging activities, including orientation programs, faculty development seminars, and participatory reading club activities. Guided by our dedicated Library Committee, we are committed to fostering a culture of learning and intellectual exploration. Welcome to your gateway to knowledge and inspiration.",
        future_plan_title="Future Plan",
        future_plan_text="The future plan for the library involves expanding its physical space and digital infrastructure to accommodate growth and enhance accessibility. This includes fully automating processes like book checkouts and inventory management, while also prioritizing the digitization of collections and integration of digital resources. Collaborative partnerships, user training, and ongoing evaluation will ensure that the library remains a cutting-edge hub for research and learning in the digital age.",
        sections_text="Reference Section\nCirculation Section\nPeriodical Section",
        about_services_text="The library has automated all its library activities to provide effective and wide range of academic resources such as books, journals, online databases.",
        new_suggestion_text="The library always encourages all students and faculty to recommend new books in order to strengthen their collection."
    )

    if copied:
        settings.library_image = dest_image_rel
        settings.save()
        print("Updated settings image field to local media path.")

    # Copy and seed gallery images
    src_img1 = os.path.join('..', 'chaitanyacg.ac.in', 'static', 'assets', 'images', 'feature', '0001.png')
    dest_img1_rel = 'library/gallery/0001.png'
    dest_img1_full = os.path.join('media', dest_img1_rel)
    
    src_img2 = os.path.join('..', 'chaitanyacg.ac.in', 'static', 'assets', 'images', 'feature', 'admission.jpg')
    dest_img2_rel = 'library/gallery/admission.jpg'
    dest_img2_full = os.path.join('media', dest_img2_rel)

    copied_g1 = False
    copied_g2 = False

    if os.path.exists(src_img1):
        try:
            shutil.copy(src_img1, dest_img1_full)
            copied_g1 = True
            print(f"Copied {src_img1} to {dest_img1_full}")
        except Exception as e:
            print(f"Error copying {src_img1}: {e}")

    if os.path.exists(src_img2):
        try:
            shutil.copy(src_img2, dest_img2_full)
            copied_g2 = True
            print(f"Copied {src_img2} to {dest_img2_full}")
        except Exception as e:
            print(f"Error copying {src_img2}: {e}")

    # Create gallery records
    if copied_g1:
        LibraryGalleryImage.objects.create(
            settings=settings,
            image=dest_img1_rel,
            caption="College Library Reading Room",
            order=1
        )
    if copied_g2:
        LibraryGalleryImage.objects.create(
            settings=settings,
            image=dest_img2_rel,
            caption="Students Accessing Learning Resources",
            order=2
        )
    print("Gallery images seeded.")

    # Categories data
    categories = [
        ("UG/PG Course Text Books", 1665, 1),
        ("Reference Books", 200, 2),
        ("Fiction/Nonfiction Books", 347, 3),
        ("Donated Books", 150, 4),
        ("Others", 229, 5),
    ]

    for cat_name, num_books, order in categories:
        LibraryBookCategory.objects.create(
            category_name=cat_name,
            num_books=num_books,
            order=order
        )
        print(f"Created category: {cat_name}")

    # Resources data
    resources = [
        ("INFLIBNET (Information and Library Network)", "https://www.inflibnet.ac.in/", 1),
        ("NLIST (National Library and Information Services Infrastructure for Scholarly Content)", "https://nlist.inflibnet.ac.in/", 2),
        ("E-PATHSALA/epg-Pathsala", "https://epgp.inflibnet.ac.in/", 3),
        ("SHODH GANGA", "https://shodhganga.inflibnet.ac.in/", 4),
        ("SHODH SINDHU", "https://shodhsindhu.inflibnet.ac.in/", 5),
        ("VIDWAN DATABASE", "https://vidwan.inflibnet.ac.in/", 6),
        ("NDL (National Digital Library)", "https://ndl.iitkgp.ac.in/", 7),
        ("E-pusthkalay", "https://epustakalay.com/", 8),
        ("MOOCs (Massive Open Online Courses)", "https://www.mooc.org/", 9),
        ("SWAYAM (Study Webs of Active Learning for Young Aspiring Minds)", "https://swayam.gov.in/", 10),
        ("NPTEL (National Programme on Technology Enhanced Learning)", "https://nptel.ac.in/", 11),
        ("National Library of India", "http://www.nationallibrary.gov.in/", 12),
        ("Gutenberg", "https://www.gutenberg.org/", 13),
        ("E-gyankosh", "https://egyankosh.ac.in/", 14),
        ("DOAJ (Directory of Open Access Journals)", "https://doaj.org/", 15),
    ]

    for name, url, order in resources:
        LibraryResource.objects.create(
            name=name,
            website_url=url,
            order=order
        )
        print(f"Created resource: {name}")

    print("Seeding finished successfully.")

if __name__ == '__main__':
    seed_library()
