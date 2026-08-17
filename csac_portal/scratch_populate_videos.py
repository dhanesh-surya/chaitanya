import os
import sys
import django
import shutil
from bs4 import BeautifulSoup
from django.core.files import File
import datetime

# Configure Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_portal.settings')
django.setup()

from django.conf import settings
from gallery.models import GalleryCategory, GalleryItem

# Reconfigure stdout for UTF-8 compatibility on Windows terminal
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def parse_date(date_str):
    if not date_str:
        return None
    date_str = date_str.strip().replace('.', '').strip()
    if date_str.upper() in ('NA', ''):
        return None
    
    # Try different formats
    for fmt in ('%B %d, %Y', '%b %d, %Y'):
        try:
            return datetime.datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    print(f"Warning: Could not parse date '{date_str}'")
    return None

def main():
    html_path = 'C:/temp-csac/chaitanyacg.ac.in/gallery/2/index.html'
    
    if not os.path.exists(html_path):
        print(f"Error: HTML file {html_path} does not exist.")
        return

    print("Parsing HTML file...")
    with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    items_divs = soup.find_all('div', class_='col-lg-4')
    print(f"Found {len(items_divs)} potential items in grid.")

    # Ensure target media folder exists
    media_videos_dir = os.path.join(settings.MEDIA_ROOT, 'gallery', 'videos')
    os.makedirs(media_videos_dir, exist_ok=True)

    # Optional: clear existing video items to prevent duplicates on repeated runs
    print("Clearing existing video items in database...")
    GalleryItem.objects.filter(gallery_type='video').delete()

    imported_count = 0

    for div in items_divs:
        single_item = div.find('div', class_='single-item')
        if not single_item:
            continue
            
        a_tag = single_item.find('a')
        img_tag = single_item.find('img')
        
        video_url = a_tag.get('href', '').strip() if a_tag else ''
        img_src = img_tag.get('src', '').strip() if img_tag else ''
        
        meta_div = single_item.find('div', class_='single-item__meta')
        if not meta_div:
            continue
            
        # Category label (e.g. Day Celebration)
        label_p = meta_div.find('p', style=lambda s: s and 'color:#B71A34' in s.replace(' ', ''))
        label = label_p.get_text(strip=True) if label_p else ''
        
        # Title
        title_h5 = meta_div.find('h5', class_='item-title')
        title = title_h5.get_text(strip=True) if title_h5 else ''
        
        # Date
        em_tag = meta_div.find('em')
        date_str = ''
        if em_tag:
            date_p = em_tag.find('p', class_='item-description')
            if date_p:
                date_str = date_p.get_text(strip=True)
        
        pub_date = parse_date(date_str)
        
        # Description
        desc_p = None
        for p in meta_div.find_all('p'):
            style = p.get('style', '') or ''
            if '#B71A34' in style:
                continue
            if p.find_parent('em'):
                continue
            text = p.get_text(strip=True)
            if not text:
                continue
            if text == date_str or text == label:
                continue
            desc_p = p
            break
            
        description = desc_p.get_text(strip=True) if desc_p else ""
        
        # Create category
        cat_name = label if label else "Video Gallery"
        category_obj, _ = GalleryCategory.objects.get_or_create(name=cat_name)

        print(f"\nProcessing Video [{imported_count+1}]: {title}")
        print(f"  URL: {video_url}")
        print(f"  Date: {pub_date} | Category: {cat_name}")
        
        item = GalleryItem(
            category=category_obj,
            gallery_type='video',
            title=title,
            description=description,
            video_url=video_url,
            date=pub_date,
            is_active=True,
            order=imported_count
        )

        # Handle local image resolution & copying
        if img_src:
            clean_rel = img_src.replace('../', '')
            abs_img_path = os.path.normpath(os.path.join('C:/temp-csac', clean_rel))
            
            if os.path.exists(abs_img_path):
                print(f"  Found local image file: {abs_img_path}")
                try:
                    with open(abs_img_path, 'rb') as img_file:
                        item.image.save(os.path.basename(abs_img_path), File(img_file), save=False)
                    print("  Saved image file locally to media folder.")
                except Exception as e:
                    print(f"  Warning: Error saving image file: {e}")
            else:
                print(f"  Warning: Local image file not found at {abs_img_path}")
                # Fallback to saving image url
                item.image_url = img_src

        item.save()
        imported_count += 1

    print(f"\nImport finished! Successfully imported {imported_count} videos.")

if __name__ == '__main__':
    main()
