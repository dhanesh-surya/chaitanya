import os
import sys

import django

sys.path.insert(0, os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "college_portal.settings")
django.setup()

from academics.models import Program, Syllabus

print("=== Program diffs (local) ===")
for p in Program.objects.order_by("pk"):
    print(p.pk, p.name, p.introduced_year, p.affiliation_status, p.seats)

print("\n=== Syllabus diffs (local) ===")
for s in Syllabus.objects.order_by("pk"):
    print(s.pk, s.title, s.document.name if s.document else "", s.document_url, s.order)