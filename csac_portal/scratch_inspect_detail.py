import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\temp-csac\chaitanyacg.ac.in\department\1\index.html"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Print all img tags
img_tags = re.findall(r'<img[^>]*src=["\'](.*?)["\'][^>]*>', content, re.IGNORECASE)
print("--- Images ---")
for img in img_tags:
    print(img)

# 2. Search for HOD / Head / message text
print("\n--- HOD / Message Mentions ---")
matches = re.findall(r'([^<>\n]{0,50}(?:hod|head|message|doctor|prof|mr\.|mrs\.|dr\.)[^<>\n]{0,50})', content, re.IGNORECASE)
for m in set(matches[:15]):
    print(m.strip())

# 3. Print all headings inside program content area
print("\n--- Headings (h3, h4, h5, h6) ---")
h_tags = re.findall(r'<(h[3456])[^>]*>(.*?)</\1>', content, re.DOTALL | re.IGNORECASE)
for tag, text in h_tags:
    clean_text = re.sub(r'<[^>]+>', '', text).strip()
    print(f"{tag}: {clean_text}")
