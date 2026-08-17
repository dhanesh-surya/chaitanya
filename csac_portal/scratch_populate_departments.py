import os
import shutil
import re
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_portal.settings')
django.setup()

from django.conf import settings
from academics.models import Department

FOLDER_TO_SLUG = {
    '1': 'hindi',
    '2': 'english',
    '3': 'sociology',
    '4': 'geography',
    '5': 'social-work',
    '6': 'zoology',
    '9': 'chemistry',
    '10': 'mathematics',
    '11': 'botany',
    '12': 'forestry',
    '13': 'political-science',
    '15': 'computer-science'
}

CORRECT_IMAGE_MAPPING = {
    'hindi': 'hindi.png',
    'english': '1.png',
    'sociology': 'sociology.png',
    'geography': 'geography.png',
    'social-work': 'socialwork.png',
    'zoology': 'zoology.png',
    'chemistry': 'chemistry.png',
    'mathematics': 'maths.png',
    'botany': 'botany.png',
    'forestry': 'Forestry.jpg',
    'political-science': 'botany.png',
    'computer-science': 'cs.png'
}

def run():
    print("Starting departments populate script...")
    
    base_html_dir = r"C:\temp-csac\chaitanyacg.ac.in\department"
    src_img_dir = r"C:\temp-csac\chaitanyafiles01.s3.amazonaws.com\departmentImages"
    dest_img_dir = os.path.join(settings.MEDIA_ROOT, 'dept', 'banner')
    os.makedirs(dest_img_dir, exist_ok=True)
    
    updated_count = 0
    
    for folder, slug in FOLDER_TO_SLUG.items():
        # Get existing department in DB
        try:
            dept = Department.objects.get(slug=slug)
        except Department.DoesNotExist:
            print(f"Error: Department with slug '{slug}' does not exist in the database. Skipping.")
            continue
            
        idx_file = os.path.join(base_html_dir, folder, "index.html")
        if not os.path.exists(idx_file):
            print(f"Error: index.html not found for folder {folder} ({slug}). Skipping.")
            continue
            
        with open(idx_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract description HTML block
        desc_match = re.search(r'<div class="program-about">(.*?)<!-- single testimonial -->', content, re.DOTALL | re.IGNORECASE)
        description = desc_match.group(1).strip() if desc_match else None
        
        if not description:
            desc_match_alt = re.search(r'<div class="program-about">(.*?)</div>', content, re.DOTALL | re.IGNORECASE)
            description = desc_match_alt.group(1).strip() if desc_match_alt else None
            
        if description:
            if description.endswith('</div>'):
                description = description[:-6].strip()
            # Clean up double line breaks and whitespace
            description = re.sub(r'\s+', ' ', description)
            # Make src paths for internal page images local if any (like icons or static assets)
            description = description.replace('../../static/assets/images/', '/static/assets/images/')
            
        # Copy the correct banner image
        filename = CORRECT_IMAGE_MAPPING.get(slug)
        if filename:
            src_image_path = os.path.join(src_img_dir, filename)
            if os.path.exists(src_image_path):
                dest_image_path = os.path.join(dest_img_dir, filename)
                try:
                    shutil.copy2(src_image_path, dest_image_path)
                    dept.banner_image = f"dept/banner/{filename}"
                    print(f"Copied banner image {filename} to local media for '{dept.name}'")
                except Exception as e:
                    print(f"Error copying banner image for '{slug}': {e}")
            else:
                print(f"Warning: Source banner image '{filename}' not found in '{src_img_dir}'")
        
        # Save description
        if description:
            dept.description = description
            
        dept.save()
        print(f"Successfully updated department: {dept.name} (slug: {slug})")
        updated_count += 1
        
    print(f"Successfully processed {updated_count} departments!")

if __name__ == '__main__':
    run()
