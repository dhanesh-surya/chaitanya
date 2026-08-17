import os
import shutil
import urllib.parse
import django

# Setup django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_portal.settings')
django.setup()

from core.models import BannerSlide

SRC_DIR = r"C:\temp-csac\chaitanyafiles01.s3.amazonaws.com\homeImages"
DEST_DIR = r"C:\temp-csac\csac_portal\media\banner"

os.makedirs(DEST_DIR, exist_ok=True)

slides = BannerSlide.objects.all()
print(f"Found {slides.count()} banner slides.")

for slide in slides:
    url = slide.image_url
    if not url:
        print(f"Slide {slide.id} has no image_url, skipping.")
        continue
    
    # Extract filename from URL (e.g. https://chaitanyafiles01.s3.amazonaws.com/homeImages/filename)
    filename = url.split("homeImages/")[-1]
    src_file_raw = os.path.join(SRC_DIR, filename)
    decoded_filename = urllib.parse.unquote(filename)
    src_file_decoded = os.path.join(SRC_DIR, decoded_filename)
    
    src_path = None
    actual_filename = None
    
    if os.path.exists(src_file_raw):
        src_path = src_file_raw
        actual_filename = filename
    elif os.path.exists(src_file_decoded):
        src_path = src_file_decoded
        actual_filename = decoded_filename
    else:
        # Try finding a match in list
        for f in os.listdir(SRC_DIR):
            if urllib.parse.unquote(f) == decoded_filename or f.lower() == filename.lower():
                src_path = os.path.join(SRC_DIR, f)
                actual_filename = f
                break
                
    if not src_path:
        print(f"Error: Image file not found for slide {slide.id} ({url}).")
        continue
        
    dest_path = os.path.join(DEST_DIR, actual_filename)
    
    # Copy the file
    try:
        shutil.copy2(src_path, dest_path)
        # In Django, ImageField stores the path relative to MEDIA_ROOT, so 'banner/filename'
        relative_path = f"banner/{actual_filename}"
        slide.image = relative_path
        slide.save()
        print(f"Updated slide {slide.id} to use local image {relative_path}")
    except Exception as e:
        print(f"Error copying/updating slide {slide.id}: {e}")

print("Done!")
