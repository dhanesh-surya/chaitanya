import os
import urllib.request
import urllib.parse
import ssl
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_portal.settings')
django.setup()

from django.conf import settings
from core.models import UGCTable, UGCDocument

def download_file(url, dest_dir):
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
    print("Starting UGC populate script...")
    
    # 1. Clear existing tables and documents
    UGCDocument.objects.all().delete()
    UGCTable.objects.all().delete()
    print("Cleared existing UGC Table & Document records.")
    
    # 2. Create the default "UGC Files" table
    default_table = UGCTable.objects.create(
        name="UGC Files",
        order=1,
        is_active=True
    )
    print(f"Created default UGC Table: '{default_table.name}'")
    
    # Destination directory
    dest_dir = os.path.join(settings.MEDIA_ROOT, 'ugc', 'documents')
    os.makedirs(dest_dir, exist_ok=True)
    
    # Document data from static archive
    documents_data = [
        {"sn": 1, "title": "Student Grievance Redressal Committee (SGRC)", "url": "https://chaitanyafiles01.s3.amazonaws.com/ugcItems/SGRC.pdf"},
        {"sn": 2, "title": "Anti-Ragging Regulations", "url": "https://chaitanyafiles01.s3.amazonaws.com/ugcItems/Anti-Ragging.pdf"},
        {"sn": 3, "title": "Institutional Development Plans (IDP)", "url": "https://chaitanyafiles01.s3.amazonaws.com/ugcItems/IDP.pdf"},
        {"sn": 4, "title": "Equity & Inclusion (SEDGs)", "url": "https://chaitanyafiles01.s3.amazonaws.com/ugcItems/SEDGs.pdf"},
        {"sn": 5, "title": "Accessibility Standards", "url": "https://chaitanyafiles01.s3.amazonaws.com/ugcItems/Accessibility.pdf"},
        {"sn": 6, "title": "Research & Development Cell", "url": "https://chaitanyafiles01.s3.amazonaws.com/ugcItems/RDC.pdf"},
        {"sn": 7, "title": "Fee Refund Policy", "url": "https://chaitanyafiles01.s3.amazonaws.com/ugcItems/Fee_Refund_Policy.pdf"},
        {"sn": 8, "title": "Public Disclosure", "url": "https://chaitanyafiles01.s3.amazonaws.com/ugcItems/Public_Disclosure.pdf"},
        {"sn": 9, "title": "Facilities for the differently abled persons", "url": "https://chaitanyafiles01.s3.amazonaws.com/ugcItems/Physically_Challenged_Students.pdf"},
        {"sn": 10, "title": "Account Audit Report_2022", "url": "https://chaitanyafiles01.s3.amazonaws.com/ugcItems/Account_Audit_Report_2022.pdf"},
        {"sn": 11, "title": "Account Audit Report_2023", "url": "https://chaitanyafiles01.s3.amazonaws.com/ugcItems/Account_Audit_Report_2023.pdf"},
        {"sn": 12, "title": "Undertaking", "url": "https://chaitanyafiles01.s3.amazonaws.com/ugcItems/UNDERTAKING__.pdf"},
        {"sn": 13, "title": "Internal Complaints Committee (ICC)", "url": "https://chaitanyafiles01.s3.amazonaws.com/ugcItems/ICC.pdf"},
    ]
    
    seeded_count = 0
    for doc in documents_data:
        filename = download_file(doc["url"], dest_dir)
        
        db_doc = UGCDocument(
            ugc_table=default_table,
            sn=doc["sn"],
            title=doc["title"],
            file_url=doc["url"]
        )
        if filename:
            db_doc.file = f"ugc/documents/{filename}"
            
        db_doc.save()
        print(f"Seeded Document: {doc['title']} (S.N. {doc['sn']})")
        seeded_count += 1
        
    print(f"Successfully seeded {seeded_count} documents in UGC Table '{default_table.name}'!")

if __name__ == '__main__':
    run()
