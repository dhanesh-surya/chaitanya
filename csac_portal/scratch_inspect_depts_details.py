import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

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

base_dir = r"C:\temp-csac\chaitanyacg.ac.in\department"
for folder, slug in FOLDER_TO_SLUG.items():
    idx_file = os.path.join(base_dir, folder, "index.html")
    if os.path.exists(idx_file):
        with open(idx_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract banner image
        # Look inside program-big-thumb or find the first img under program-description-area
        banner_match = re.search(r'<div class="program-big-thumb">\s*<img[^>]*src=["\'](.*?)["\']', content, re.DOTALL | re.IGNORECASE)
        banner_src = banner_match.group(1) if banner_match else None
        banner_file = os.path.basename(banner_src) if banner_src else None
        
        # Extract program-about description
        # We search from <div class="program-about"> to the next <!-- single testimonial -->
        desc_match = re.search(r'<div class="program-about">(.*?)<!-- single testimonial -->', content, re.DOTALL | re.IGNORECASE)
        description = desc_match.group(1).strip() if desc_match else None
        
        # If the above fails, let's try searching up to the next </div> that closes program-about
        if not description:
            desc_match_alt = re.search(r'<div class="program-about">(.*?)</div>', content, re.DOTALL | re.IGNORECASE)
            description = desc_match_alt.group(1).strip() if desc_match_alt else None
            
        desc_len = len(description) if description else 0
        
        # Clean up description (strip trailing </div> if present)
        if description and description.endswith('</div>'):
            description = description[:-6].strip()
            
        print(f"Folder: {folder} | Slug: {slug} | Banner Image: {banner_file} | Desc Len: {desc_len}")
    else:
        print(f"Folder: {folder} | Slug: {slug} | File not found")
