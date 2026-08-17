import os
import urllib.request
import urllib.parse
import django
from html.parser import HTMLParser

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_portal.settings')
django.setup()

from django.conf import settings
from core.models import Policy

class PolicyParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_tbody = False
        self.in_tr = False
        self.in_td = False
        self.current_row = []
        self.current_td_text = []
        self.current_href = None
        self.rows = []

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.in_table = True
        elif tag == 'tbody' and self.in_table:
            self.in_tbody = True
        elif tag == 'tr' and self.in_tbody:
            self.in_tr = True
            self.current_row = []
        elif tag == 'td' and self.in_tr:
            self.in_td = True
            self.current_td_text = []
            self.current_href = None
        elif tag == 'a' and self.in_td:
            attrs_dict = dict(attrs)
            if 'href' in attrs_dict:
                self.current_href = attrs_dict['href']

    def handle_endtag(self, tag):
        if tag == 'table':
            self.in_table = False
            self.in_tbody = False
        elif tag == 'tbody':
            self.in_tbody = False
        elif tag == 'tr' and self.in_tr:
            self.in_tr = False
            if self.current_row:
                self.rows.append(self.current_row)
        elif tag == 'td' and self.in_td:
            self.in_td = False
            text = "".join(self.current_td_text).strip()
            self.current_row.append({
                'text': text,
                'href': self.current_href
            })

    def handle_data(self, data):
        if self.in_td:
            self.current_td_text.append(data)

def download_file(url, dest_dir):
    import ssl
    os.makedirs(dest_dir, exist_ok=True)
    parsed_url = urllib.parse.urlparse(url)
    filename = os.path.basename(parsed_url.path)
    filename = urllib.parse.unquote(filename)
    dest_path = os.path.join(dest_dir, filename)
    
    print(f"Downloading {url} -> {dest_path}")
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, timeout=30, context=context) as response:
            with open(dest_path, 'wb') as out_file:
                out_file.write(response.read())
        print(f"Successfully downloaded {filename}")
        return filename
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None


def run():
    print("Starting policies populate script...")
    html_path = r"C:\temp-csac\chaitanyacg.ac.in\policies.html"
    if not os.path.exists(html_path):
        print(f"Error: policies.html not found at {html_path}")
        return

    parser = PolicyParser()
    with open(html_path, 'r', encoding='utf-8') as f:
        parser.feed(f.read())

    print(f"Found {len(parser.rows)} raw table rows in HTML.")

    # Clear existing policies
    Policy.objects.all().delete()
    print("Cleared existing Policy records.")

    dest_dir = os.path.join(settings.MEDIA_ROOT, 'policies')
    os.makedirs(dest_dir, exist_ok=True)

    imported_count = 0
    for idx, row in enumerate(parser.rows):
        if len(row) < 3:
            continue
        
        sn_cell = row[0]
        title_cell = row[1]
        doc_cell = row[2]
        
        title = title_cell['text'].strip()
        url = doc_cell['href']
        
        if not title or not url:
            print(f"Skipping row {idx}: Title or URL missing ({title}, {url})")
            continue
            
        try:
            order = int(sn_cell['text'].strip())
        except ValueError:
            order = idx + 1
            
        # Download the policy file
        filename = download_file(url, dest_dir)
        
        policy = Policy(
            title=title,
            document_url=url,
            order=order
        )
        if filename:
            policy.document = f"policies/{filename}"
        else:
            print(f"Warning: Could not download local file for policy '{title}', saving url only.")
            
        policy.save()
        print(f"Created Policy: {title} (Order: {order})")
        imported_count += 1

    print(f"Successfully seeded {imported_count} policies!")

if __name__ == '__main__':
    run()
