import hashlib
import json
import os
import sys

import django

sys.path.insert(0, os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "college_portal.settings")
django.setup()

from academics.models import Department, DepartmentFaculty, Program, Syllabus


def sig(qs, fields):
    payload = [
        (obj.pk,) + tuple(getattr(obj, field) for field in fields)
        for obj in qs.order_by("pk")
    ]
    return hashlib.md5(json.dumps(payload, default=str).encode()).hexdigest()


print("dept", sig(Department.objects.all(), ["name", "slug", "order"]))
print("prog", sig(Program.objects.all(), ["name", "program_type", "order"]))
print("fac", sig(DepartmentFaculty.objects.all(), ["name", "designation", "order"]))
print("syl", sig(Syllabus.objects.all(), ["title", "document", "document_url", "order"]))