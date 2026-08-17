import os
import re
import sys

# Reconfigure stdout to support unicode
sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"C:\temp-csac\chaitanyacg.ac.in\department"
for item in sorted(os.listdir(base_dir), key=lambda x: int(x) if x.isdigit() else 999):
    item_path = os.path.join(base_dir, item)
    if os.path.isdir(item_path):
        idx_file = os.path.join(item_path, "index.html")
        if os.path.exists(idx_file):
            with open(idx_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find the html title
            title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL | re.IGNORECASE)
            title = title_match.group(1).strip() if title_match else "N/A"
            
            # Find breadcrumb title
            bc_match = re.search(r'<h2 class="section-title"[^>]*>\s*(.*?)\s*</h2>', content, re.DOTALL | re.IGNORECASE)
            breadcrumb = bc_match.group(1).strip() if bc_match else "N/A"
            breadcrumb = re.sub(r'\s+', ' ', breadcrumb)
            
            # Find the headline (rts-section-title)
            headline_match = re.search(r'class="rts-section-title"[^>]*>(.*?)</h3>', content, re.DOTALL | re.IGNORECASE)
            headline = headline_match.group(1).strip() if headline_match else "N/A"
            headline = re.sub(r'<[^>]+>', '', headline)
            headline = re.sub(r'\s+', ' ', headline)
            
            print(f"Folder: {item} | Title: {title} | Breadcrumb: {breadcrumb} | Headline: {headline[:40]}...")
        else:
            print(f"Folder: {item} | index.html not found")


