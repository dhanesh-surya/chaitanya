"""
Download all syllabus PDFs from S3 and store them locally in media/syllabus/.
Updates each Syllabus record to use the local file instead of the external URL.
"""
import os
import sys
import urllib.request
import urllib.error
import django

sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_portal.settings')
django.setup()

from academics.models import Syllabus
from django.conf import settings


def download_syllabus_pdfs():
    media_syllabus_dir = os.path.join(settings.MEDIA_ROOT, 'syllabus')
    os.makedirs(media_syllabus_dir, exist_ok=True)

    syllabi = Syllabus.objects.all()
    print(f"Found {syllabi.count()} syllabus entries to process.\n")

    success = 0
    failed = 0

    for s in syllabi:
        url = s.document_url
        if not url:
            print(f"  [{s.order:2d}] SKIP (no URL): {s.title}")
            continue

        # Derive a clean filename from the URL
        filename = url.rsplit('/', 1)[-1]
        # URL-decode percent-encoded characters
        filename = urllib.parse.unquote(filename)
        local_rel_path = f'syllabus/{filename}'
        local_abs_path = os.path.join(settings.MEDIA_ROOT, local_rel_path)

        # Download the PDF
        try:
            print(f"  [{s.order:2d}] Downloading: {filename} ... ", end='', flush=True)
            urllib.request.urlretrieve(url, local_abs_path)
            file_size_kb = os.path.getsize(local_abs_path) / 1024
            print(f"OK ({file_size_kb:.0f} KB)")

            # Update the record: set local file, clear external URL
            s.document.name = local_rel_path
            s.document_url = ''
            s.save()
            success += 1

        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
            print(f"FAILED ({e})")
            failed += 1

    print(f"\nDone! Downloaded: {success}, Failed: {failed}")
    print(f"Local PDF folder: {media_syllabus_dir}")


if __name__ == '__main__':
    download_syllabus_pdfs()
