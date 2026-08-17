import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_portal.settings')
django.setup()

from academics.models import Department, DepartmentBanner

depts = Department.objects.all()
migrated_count = 0

for dept in depts:
    if dept.banner_image:
        image_name = dept.banner_image.name
        if not DepartmentBanner.objects.filter(department=dept, image=image_name).exists():
            banner = DepartmentBanner.objects.create(
                department=dept,
                image=dept.banner_image,
                caption=f"{dept.name} Department",
                order=0
            )
            print(f"Created banner for {dept.name}: {image_name}")
            migrated_count += 1
        else:
            print(f"Banner for {dept.name} already exists.")
    else:
        print(f"No banner image for {dept.name}")

print(f"Successfully migrated {migrated_count} department banners.")
