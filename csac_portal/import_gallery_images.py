import os
import re
import sys
import shutil
import django
from datetime import date

# Configure Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "college_portal.settings")
django.setup()

from gallery.models import GalleryCategory, GalleryItem
from PIL import Image, ImageDraw, ImageFont

# Reconfigure stdout for UTF-8 compatibility on Windows terminal
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Mapping for month strings to integers
month_map = {
    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
    'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
}

def parse_date(date_str):
    if not date_str or date_str.strip().lower() in ['none', 'na', '']:
        return None
    date_str = date_str.strip().lower()
    # Replace dots and commas with spaces and remove extra spaces
    date_str = re.sub(r'[\.\s,]+', ' ', date_str).strip()
    parts = date_str.split()
    if len(parts) >= 3:
        m_str, d_str, y_str = parts[0], parts[1], parts[2]
        month_num = None
        for k, v in month_map.items():
            if m_str.startswith(k):
                month_num = v
                break
        if month_num:
            try:
                day_num = int(d_str)
                year_num = int(y_str)
                return date(year_num, month_num, day_num)
            except ValueError:
                pass
    return None

def create_placeholder_image(dest_path, filename, title, category):
    """
    Creates a clean, styled placeholder image using PIL when the original file is missing.
    """
    width, height = 800, 600
    # Create image with college branding color theme (dark red/burgundy accent)
    img = Image.new('RGB', (width, height), color='#f4f5f7')
    draw = ImageDraw.Draw(img)
    
    # Draw border
    draw.rectangle([10, 10, width - 10, height - 10], outline='#e61013', width=3)
    
    # Try to load Arial font, fall back to default
    try:
        title_font = ImageFont.truetype("arial.ttf", 36)
        meta_font = ImageFont.truetype("arial.ttf", 22)
    except IOError:
        title_font = ImageFont.load_default()
        meta_font = ImageFont.load_default()
        
    # Draw texts
    draw.text((50, 80), "CHAITANYA SCIENCE & ARTS COLLEGE", fill='#e61013', font=meta_font)
    draw.text((50, 120), "OFFLINE GALLERY PLACEHOLDER", fill='#1a1a1a', font=title_font)
    
    draw.line([50, 190, width - 50, 190], fill='#e61013', width=2)
    
    draw.text((50, 230), f"File Name: {filename}", fill='#333333', font=meta_font)
    draw.text((50, 280), f"Title: {title}", fill='#333333', font=meta_font)
    draw.text((50, 330), f"Category: {category}", fill='#333333', font=meta_font)
    draw.text((50, 380), "Status: Image file missing from source backup - auto-generated", fill='#b71a34', font=meta_font)
    
    img.save(dest_path)
    print(f"Generated placeholder image at {dest_path}")

def main():
    html_path = r"C:\temp-csac\chaitanyacg.ac.in\gallery\1\index.html"
    s3_dir = r"C:\temp-csac\chaitanyafiles01.s3.amazonaws.com\gallery"
    target_media_dir = r"C:\temp-csac\csac_portal\media\gallery\images"
    
    # Ensure target directory exists
    os.makedirs(target_media_dir, exist_ok=True)
    
    if not os.path.exists(html_path):
        print(f"Error: HTML path {html_path} does not exist.")
        return
        
    with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # Split content to locate each card
    cards = content.split('<div class="single-item"')[1:]
    print(f"Parsed {len(cards)} items from HTML file.")
    
    # Delete existing Image Gallery items in database to start clean
    print("Clearing existing Image Gallery items from the database...")
    deleted_count, _ = GalleryItem.objects.filter(category__gallery_type='image').delete()
    print(f"Deleted {deleted_count} items.")
    
    imported_count = 0
    copied_count = 0
    placeholder_count = 0
    
    for idx, card in enumerate(cards, 1):
        # Extract the card's inner content
        card_content = card.split('</div>\n</div>\n</div>\n</div>')[0]
        
        # 1. Extract image filename from the img tag src
        img_match = re.search(r'<img\s+[^>]*src="([^"]+)"', card_content)
        img_src = img_match.group(1) if img_match else ""
        filename = os.path.basename(img_src) if img_src else ""
        
        if not filename:
            print(f"Warning: Item {idx} has no image source filename. Skipping.")
            continue
            
        # 2. Extract and normalize category
        # <p class="item-description" style="font-size:15px;color:#B71A34">Cultural Activities</p>
        cat_match = re.search(r'color:\s*#B71A34[^>]*>(.*?)</p>', card_content, re.IGNORECASE)
        category_name = cat_match.group(1).strip() if cat_match else ""
        if not category_name:
            category_name = "General"
        elif category_name.lower() in ["fied visit", "fiedvisit"]:
            category_name = "Field Visit"
            
        # 3. Extract title
        title = ""
        title_match = re.search(r'<h5 class="item-title">.*?>(.*?)</a></h5>', card_content, re.DOTALL)
        if not title_match:
            title_match = re.search(r'<h5 class="item-title">(.*?)</h5>', card_content, re.DOTALL)
        if title_match:
            title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
        if not title or title.lower() == "none":
            title = "Gallery Image"
            
        # 4. Extract and parse date
        date_str = ""
        date_match = re.search(r'<em>.*?style="font-size:15px;[^"]*">(.*?)</p>.*?</em>', card_content, re.DOTALL)
        if not date_match:
            date_match = re.search(r'<em>(.*?)</em>', card_content, re.DOTALL)
        if date_match:
            date_str = re.sub(r'<[^>]+>', '', date_match.group(1)).strip()
        parsed_date = parse_date(date_str)
        
        # 5. Extract description
        desc = ""
        desc_match = re.search(r'<p class="item-description"></p><p>(.*?)</p>', card_content, re.DOTALL)
        if desc_match:
            desc = re.sub(r'<[^>]+>', '', desc_match.group(1)).strip()
        if desc.lower() == "na":
            desc = ""
            
        # 6. Copy file / create placeholder
        source_file = os.path.join(s3_dir, filename)
        dest_file = os.path.join(target_media_dir, filename)
        
        if os.path.exists(source_file):
            shutil.copy2(source_file, dest_file)
            copied_count += 1
        else:
            create_placeholder_image(dest_file, filename, title, category_name)
            placeholder_count += 1
            
        # 7. Database entry
        cat_obj, _ = GalleryCategory.objects.get_or_create(
            name=category_name,
            gallery_type='image'
        )
        
        GalleryItem.objects.create(
            category=cat_obj,
            title=title,
            description=desc,
            image=f"gallery/images/{filename}",
            image_url=f"https://chaitanyafiles01.s3.amazonaws.com/gallery/{filename}",
            date=parsed_date,
            is_active=True
        )
        imported_count += 1
        
    print(f"\nImport Summary:")
    print(f"Total processed/imported: {imported_count}")
    print(f"Files copied: {copied_count}")
    print(f"Placeholders generated: {placeholder_count}")

if __name__ == "__main__":
    main()
