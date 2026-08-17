import os
import re

file_path = r'C:\temp-csac\chaitanyacg.ac.in\index.html'
with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Locate the right bottom banner block
start_match = re.search(r'class=["\']banner__content__bottom__right o-hidden["\']', html)
if start_match:
    start_pos = start_match.start()
    # Let's extract the next 50000 characters which should contain the swiper
    block = html[start_pos:start_pos+50000]
    
    # Find all swiper-slides in this block
    slides = re.findall(r'<div class=["\']swiper-slide["\']([\s\S]+?)</div>\s*</div>', block)
    if not slides:
        # Fallback regex to just capture slides content inside swiper-wrapper
        slides = re.findall(r'<div class=["\']swiper-slide["\'][\s\S]*?>([\s\S]+?)</div>\s*</div>', block)
    
    # Let's find all images and captions inside
    # We can also just search for all <div class="swiper-slide"> ... </div> structures
    # Let's use a non-greedy findall for swiper-slide
    swiper_slides = re.findall(r'<div class=["\']swiper-slide["\']>([\s\S]+?)</div>\s*</div>', block)
    
    # Wait, let's write a simple loop to find slides
    # Let's split by '<div class="swiper-slide">' and look at the contents
    parts = block.split('class="swiper-slide"')
    print(f"Total parts split by swiper-slide: {len(parts) - 1}")
    for idx, part in enumerate(parts[1:]):
        # We only care about the content of this slide before the next slide/container closes
        # Find img src and caption
        img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', part)
        alt_match = re.search(r'<img[^>]+alt=["\']([^"\']*)["\']', part)
        cap_match = re.search(r'class=["\']caption["\'][^>]*>([^<]+)', part)
        
        img_src = img_match.group(1) if img_match else 'None'
        img_alt = alt_match.group(1) if alt_match else 'None'
        caption = cap_match.group(1).strip() if cap_match else 'None'
        
        print(f"Slide {idx+1}:")
        print(f"  Img: {img_src}")
        print(f"  Alt: {img_alt}")
        print(f"  Caption: {caption}")
else:
    print("Could not find right bottom banner block")
