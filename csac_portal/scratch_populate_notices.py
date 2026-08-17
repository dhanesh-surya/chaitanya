import os
import sys
import django
import requests
from bs4 import BeautifulSoup
from django.core.files import File
import tempfile
from urllib.parse import urlparse
import datetime

# Configure Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_portal.settings')
django.setup()

from django.conf import settings
from core.models import Notice

# Reconfigure stdout for UTF-8 compatibility on Windows terminal
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    html_path = 'C:/temp-csac/chaitanyacg.ac.in/notices/index.html'
    
    if not os.path.exists(html_path):
        print(f"Error: HTML file {html_path} does not exist.")
        return

    print("Parsing HTML file...")
    with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Ensure target media folder exists
    media_notices_dir = os.path.join(settings.MEDIA_ROOT, 'notices')
    os.makedirs(media_notices_dir, exist_ok=True)

    # Helper function to extract notice items from a tab
    def extract_tab_items(tab_id):
        tab = soup.find(id=tab_id)
        if not tab:
            print(f"Warning: Tab id '{tab_id}' not found.")
            return []
        items = []
        for li in tab.find_all('li', class_='single-notice'):
            date_div = li.find('div', class_='notice-date')
            if not date_div:
                continue
            day_text = "".join([t for t in date_div.contents if isinstance(t, str) or (t.name != 'span')]).strip()
            span_el = date_div.find('span')
            month_text = span_el.get_text(strip=True) if span_el else "Jan"
            
            content_div = li.find('div', class_='notice-content')
            if not content_div:
                continue
            a_tag = content_div.find('a')
            if not a_tag:
                continue
                
            title = a_tag.get_text(strip=True)
            link = a_tag.get('href', '').strip()
            
            try:
                day_val = int(day_text)
            except ValueError:
                day_val = 1
                
            items.append({
                'day': day_val,
                'month_str': month_text,
                'title': title,
                'link': link
            })
        return items

    print("Extracting categorized tabs...")
    exam_items = extract_tab_items('pills-Exam')
    admission_items = extract_tab_items('pills-Admission')
    students_items = extract_tab_items('pills-Students')
    latest_items = extract_tab_items('pills-home')

    print(f"Found {len(exam_items)} Exam notices.")
    print(f"Found {len(admission_items)} Admission notices.")
    print(f"Found {len(students_items)} Students notices.")
    print(f"Found {len(latest_items)} Latest notices.")

    # Create category mapping based on (title, link)
    category_lookup = {}
    for item in exam_items:
        category_lookup[(item['title'], item['link'])] = 'exam'
    for item in admission_items:
        category_lookup[(item['title'], item['link'])] = 'admission'
    for item in students_items:
        category_lookup[(item['title'], item['link'])] = 'students'

    month_map = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }

    # Clear existing notices in the database to do a clean seed
    print("Clearing existing Notice table from database...")
    Notice.objects.all().delete()

    current_year = 2026
    prev_month_idx = None
    imported_count = 0

    for item in latest_items:
        title = item['title']
        link = item['link']
        day = item['day']
        month_str = item['month_str']
        month_idx = month_map.get(month_str, 1)

        # Detect year transition (going backwards in time)
        if prev_month_idx is not None and month_idx > prev_month_idx:
            current_year -= 1
        prev_month_idx = month_idx

        pub_date = datetime.date(current_year, month_idx, day)
        category = category_lookup.get((title, link), 'latest')

        print(f"\n[{imported_count + 1}] Processing: {title}")
        print(f"    Date: {pub_date} | Category: {category} | URL: {link}")

        notice = Notice(
            title=title,
            category=category,
            published_date=pub_date,
            is_active=True
        )

        # Download file if it is an external URL and not a page link
        if link.startswith('http') and not link.endswith('.html') and not link.endswith('/'):
            download_url = link.replace('chaitanyafiles.s3.amazonaws.com', 'chaitanyafiles01.s3.amazonaws.com')
            notice.document_url = link
            try:
                print(f"    Downloading external attachment: {download_url}")
                response = requests.get(download_url, stream=True, timeout=20)
                if response.status_code == 200:
                    parsed_url = urlparse(download_url)
                    filename = os.path.basename(parsed_url.path)
                    if not filename:
                        ext = '.pdf' if 'pdf' in response.headers.get('content-type', '').lower() else '.jpg'
                        filename = f"notice_{day}_{month_str}_{current_year}{ext}"
                    
                    # Create temporary file to write binary chunk stream
                    lf = tempfile.TemporaryFile()
                    for chunk in response.iter_content(chunk_size=4096):
                        if chunk:
                            lf.write(chunk)
                    lf.seek(0)
                    
                    notice.document.save(filename, File(lf), save=False)
                    lf.close()
                    print(f"    Saved document locally as media/notices/{filename}")
                else:
                    print(f"    Warning: Download failed with status code {response.status_code}")
            except Exception as e:
                print(f"    Warning: Error downloading file: {e}")
        else:
            # Save the link directly as document_url for relative/webpage links
            notice.document_url = link
            print("    Skipping file download for web/page link.")

        notice.save()
        imported_count += 1

    print(f"\nImport finished! Successfully imported {imported_count} notices.")

if __name__ == '__main__':
    main()
