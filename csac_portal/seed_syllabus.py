"""
Seed script to populate Syllabus data from the static HTML source.
The source data comes from C:/chaitanyacg.ac.in/programs/syllabus/index.html.
Each entry has a program title and an S3 PDF URL.
We store these as document_url entries in the Syllabus model.
"""
import os
import sys
import django

sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_portal.settings')
django.setup()

from academics.models import Syllabus, Department


# Syllabus data extracted from the source HTML file
SYLLABUS_DATA = [
    {
        'order': 1,
        'title': 'DCA I, II Sem',
        'document_url': 'https://chaitanyafiles01.s3.amazonaws.com/chaitanyadoc/DCA_Syllbus.pdf',
    },
    {
        'order': 2,
        'title': 'M.A. Geography I, II Sem',
        'document_url': 'https://chaitanyafiles01.s3.amazonaws.com/chaitanyadoc/Geography_Syllabus.pdf',
    },
    {
        'order': 3,
        'title': 'M.A. English I, II Sem',
        'document_url': 'https://chaitanyafiles01.s3.amazonaws.com/chaitanyadoc/M.A._English_Syllabus.pdf',
    },
    {
        'order': 4,
        'title': 'MA Political Science I, II Sem',
        'document_url': 'https://chaitanyafiles01.s3.amazonaws.com/chaitanyadoc/M._A._Political_Science_Syllabus.pdf',
    },
    {
        'order': 5,
        'title': 'M. A. Sociology I, II Sem',
        'document_url': 'https://chaitanyafiles01.s3.amazonaws.com/chaitanyadoc/M._A._Sociology_Syllabus.pdf',
    },
    {
        'order': 6,
        'title': 'M.Com I, II Sem',
        'document_url': 'https://chaitanyafiles01.s3.amazonaws.com/chaitanyadoc/M.COM_Syllabus.pdf',
    },
    {
        'order': 7,
        'title': 'M.Sc. Botany I, II Sem',
        'document_url': 'https://chaitanyafiles01.s3.amazonaws.com/chaitanyadoc/M.Sc._Botany_Syllabus.pdf',
    },
    {
        'order': 8,
        'title': 'M.Sc. Chemistry I, II Sem',
        'document_url': 'https://chaitanyafiles01.s3.amazonaws.com/chaitanyadoc/M.Sc._Chemistry_Syllabus.pdf',
    },
    {
        'order': 9,
        'title': 'M.Sc. Computer Science I, II Sem',
        'document_url': 'https://chaitanyafiles01.s3.amazonaws.com/chaitanyadoc/M.Sc_Computer_Science_Syllabus.pdf',
    },
    {
        'order': 10,
        'title': 'M.Sc. Mathematics I, II Sem',
        'document_url': 'https://chaitanyafiles01.s3.amazonaws.com/chaitanyadoc/M.Sc_Mathematics_Syllabus.pdf',
    },
    {
        'order': 11,
        'title': 'M.Sc. Physics I, II Sem',
        'document_url': 'https://chaitanyafiles01.s3.amazonaws.com/chaitanyadoc/M.Sc._physics_syllabus.pdf',
    },
    {
        'order': 12,
        'title': 'M.Sc. Zoology I, II Sem',
        'document_url': 'https://chaitanyafiles01.s3.amazonaws.com/chaitanyadoc/M.Sc._Zoology_Syllabus.pdf',
    },
    {
        'order': 13,
        'title': 'MSW I, II Sem',
        'document_url': 'https://chaitanyafiles01.s3.amazonaws.com/chaitanyadoc/MSW_Syllabus.pdf',
    },
    {
        'order': 14,
        'title': 'PGDCA I, II Sem',
        'document_url': 'https://chaitanyafiles01.s3.amazonaws.com/chaitanyadoc/PGDCA_Syllabus.pdf',
    },
    {
        'order': 15,
        'title': 'B.A Second Semester Syllabus',
        'document_url': 'https://chaitanyafiles01.s3.amazonaws.com/chaitanyadoc/UG_Arts_Second_Semester_Syllabus.pdf',
    },
    {
        'order': 16,
        'title': 'BBA Second Semester Syllabus',
        'document_url': 'https://chaitanyafiles01.s3.amazonaws.com/chaitanyadoc/UG_BBA_Second_Semester_Syllabus.pdf',
    },
    {
        'order': 17,
        'title': 'BCA Second Semester Syllabus',
        'document_url': 'https://chaitanyafiles01.s3.amazonaws.com/chaitanyadoc/UG_BCA_Second_Semester_Syllabus.pdf',
    },
    {
        'order': 18,
        'title': 'B.Com Second Semester Syllabus',
        'document_url': 'https://chaitanyafiles01.s3.amazonaws.com/chaitanyadoc/UG_B.Com_Second_Semester_Syllabus.pdf',
    },
    {
        'order': 19,
        'title': 'B.Sc. Bio Second Semester Syllabus',
        'document_url': 'https://chaitanyafiles01.s3.amazonaws.com/chaitanyadoc/UG_Bio_Second_Semester_Syllabus.pdf',
    },
    {
        'order': 20,
        'title': 'B.Sc. (Maths) Second Semester Syllabus',
        'document_url': 'https://chaitanyafiles01.s3.amazonaws.com/chaitanyadoc/UG_Maths_Second_Semester_Syllabus.pdf',
    },
]

# Map syllabus titles to department names (best-effort matching)
TITLE_TO_DEPT = {
    'DCA I, II Sem': 'Computer Science',
    'M.A. Geography I, II Sem': 'Geography',
    'M.A. English I, II Sem': 'English',
    'MA Political Science I, II Sem': 'Political Science',
    'M. A. Sociology I, II Sem': 'Sociology',
    'M.Com I, II Sem': None,  # Commerce - may not have a department
    'M.Sc. Botany I, II Sem': 'Botany',
    'M.Sc. Chemistry I, II Sem': 'Chemistry',
    'M.Sc. Computer Science I, II Sem': 'Computer Science',
    'M.Sc. Mathematics I, II Sem': 'Mathematics',
    'M.Sc. Physics I, II Sem': 'Physics',
    'M.Sc. Zoology I, II Sem': 'Zoology',
    'MSW I, II Sem': 'Social Work',
    'PGDCA I, II Sem': 'Computer Science',
    'B.A Second Semester Syllabus': None,  # Multi-department
    'BBA Second Semester Syllabus': None,
    'BCA Second Semester Syllabus': 'Computer Science',
    'B.Com Second Semester Syllabus': None,
    'B.Sc. Bio Second Semester Syllabus': None,  # Multi-department
    'B.Sc. (Maths) Second Semester Syllabus': 'Mathematics',
}


def seed_syllabus():
    print("Seeding Syllabus data...")
    print(f"Clearing {Syllabus.objects.count()} existing syllabus entries...")
    Syllabus.objects.all().delete()

    # Get all departments for mapping
    departments = {dept.name: dept for dept in Department.objects.all()}
    print(f"Found departments: {list(departments.keys())}")

    # Use the first department as fallback for entries that don't map to a specific department
    fallback_dept = Department.objects.first()
    if not fallback_dept:
        print("ERROR: No departments found in the database. Please seed departments first.")
        return

    created_count = 0
    for entry in SYLLABUS_DATA:
        dept_name = TITLE_TO_DEPT.get(entry['title'])
        department = departments.get(dept_name, fallback_dept) if dept_name else fallback_dept

        syllabus_obj = Syllabus.objects.create(
            department=department,
            title=entry['title'],
            document_url=entry['document_url'],
            order=entry['order'],
        )
        created_count += 1
        print(f"  [{entry['order']:2d}] Created: {syllabus_obj.title} -> Dept: {department.name}")

    print(f"\nDone! Created {created_count} syllabus entries.")


if __name__ == '__main__':
    seed_syllabus()
