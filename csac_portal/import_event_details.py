import os
import re
import django
import sys
from datetime import date

# Configure Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "college_portal.settings")
django.setup()

from core.models import Happening

# Set stdout encoding to UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

month_map = {
    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
    'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
}

def parse_date(date_str):
    if not date_str:
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

def main():
    base_dir = r'C:\temp-csac\chaitanyacg.ac.in\event-details'
    happenings = Happening.objects.all()
    updated_count = 0
    
    print(f"Starting import of event details for {happenings.count()} Happenings...")
    
    for h in happenings:
        if not h.link:
            continue
        
        # Extract folder ID from link (e.g. /event-details/148/index.html -> 148)
        match = re.search(r'/event-details/(\d+)/', h.link)
        if not match:
            continue
            
        event_id = match.group(1)
        file_path = os.path.join(base_dir, event_id, 'index.html')
        
        if not os.path.exists(file_path):
            print(f"Warning: File not found for Happening {h.id} (ID: {event_id}) at {file_path}")
            continue
            
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()
            
        # 1. Parse description
        desc = ""
        desc_match = re.search(r'About The Event</h4>\s*<p class="description"></p>\s*([\s\S]+?)\s*</div>', html, re.I)
        if desc_match:
            desc = desc_match.group(1).strip()
        else:
            desc_match = re.search(r'About The Event</h4>\s*([\s\S]+?)\s*</div>', html, re.I)
            if desc_match:
                desc = desc_match.group(1).strip()
        
        # 2. Parse date
        date_match = re.search(r'Date:</div>\s*<div class="right-side">\s*<span class="desc">([^<]+)</span>', html, re.I)
        parsed_d = None
        if date_match:
            parsed_d = parse_date(date_match.group(1))
            
        # 3. Parse participants
        part_match = re.search(r'Total Participants:</div>\s*<div class="right-side">\s*<span class="desc">([\d\.]+)</span>', html, re.I)
        participants = None
        if part_match:
            try:
                participants = int(float(part_match.group(1)))
            except ValueError:
                pass
                
        # 4. Parse registration link
        reg_match = re.search(r'href=["\'](https://docs\.google\.com/forms/[^"\']+)["\']', html, re.I)
        reg_link = reg_match.group(1) if reg_match else ""
        
        # Update model
        h.description = desc
        if parsed_d:
            h.date = parsed_d
        if participants is not None:
            h.participants_count = participants
        if reg_link:
            h.registration_link = reg_link
            
        h.save()
        updated_count += 1
        print(f"Updated Happening {h.id} (ID: {event_id}): Date={h.date}, Participants={h.participants_count}, HasDesc={bool(desc)}")

    print(f"Completed! Successfully updated details for {updated_count} Happenings.")

if __name__ == "__main__":
    main()
