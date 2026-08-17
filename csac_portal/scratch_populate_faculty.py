import os
import django
import html.parser

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_portal.settings')
django.setup()

from academics.models import Department, DepartmentFaculty

class StaffHTMLParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.current_cell_data = []
        self.current_row_cells = []
        self.rows = []

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.in_table = True
        elif tag == 'tr' and self.in_table:
            self.in_row = True
            self.current_row_cells = []
        elif tag in ['td', 'th'] and self.in_row:
            self.in_cell = True
            self.current_cell_data = []

    def handle_endtag(self, tag):
        if tag == 'table':
            self.in_table = False
        elif tag == 'tr' and self.in_row:
            self.in_row = False
            self.rows.append(self.current_row_cells)
        elif tag in ['td', 'th'] and self.in_cell:
            self.in_cell = False
            self.current_row_cells.append(" ".join(self.current_cell_data).strip())

    def handle_data(self, data):
        if self.in_cell:
            self.current_cell_data.append(data.strip())

def run():
    print("Starting teaching staff import script...")
    
    # Parse HTML file
    file_path = "C:/temp-csac/chaitanyacg.ac.in/staff/1/index.html"
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    parser = StaffHTMLParser()
    with open(file_path, 'r', encoding='utf-8') as f:
        parser.feed(f.read())

    # Skip header row (row 0)
    data_rows = parser.rows[1:]
    print(f"Found {len(data_rows)} data rows to import.")

    # Departments mapping / creation
    # Existing in DB: Hindi, English, Sociology, Geography, Social Work, Political Science, History, Zoology, Physics, Chemistry, Mathematics, Botany, Forestry, Computer Science.
    # We need to create: Commerce & Management, Economics, Music.
    
    # Pre-create missing departments
    dept_creations = [
        ("Commerce & Management", "commerce-management", "commerce"),
        ("Economics", "economics", "arts"),
        ("Music", "music", "arts")
    ]
    
    for name, slug, category in dept_creations:
        dept, created = Department.objects.get_or_create(
            slug=slug,
            defaults={
                'name': name,
                'category': category,
                'order': 50 # Default high order
            }
        )
        if created:
            print(f"Created Department: {name}")

    # Load all departments into a dictionary for quick lookup by name case-insensitively
    dept_dict = {}
    for d in Department.objects.all():
        dept_dict[d.name.lower().strip()] = d

    # Special mapping for "Computer" -> "Computer Science"
    if "computer science" in dept_dict:
        dept_dict["computer"] = dept_dict["computer science"]

    # Clear existing faculty to avoid duplicates
    DepartmentFaculty.objects.all().delete()
    print("Cleared existing DepartmentFaculty records.")

    imported_count = 0
    for i, row in enumerate(data_rows):
        if len(row) < 4:
            print(f"Skipping row {i} due to insufficient columns: {row}")
            continue

        sno_str, name, post, dept_name = row
        sno_str = sno_str.strip()
        name = name.strip()
        post = post.strip()
        dept_name = dept_name.strip()

        if not name or not post or not dept_name:
            print(f"Skipping row {i} due to empty fields: {row}")
            continue

        # Get order from sno
        try:
            order = int(sno_str)
        except ValueError:
            order = i + 1

        # Look up department
        dept_key = dept_name.lower().strip()
        dept = dept_dict.get(dept_key)
        
        if not dept:
            # Create department on the fly
            slug = dept_name.lower().replace('&', 'and').replace(' ', '-').replace('--', '-')
            # Determine category choice
            category = 'science' if dept_name.lower() in ['chemistry', 'physics', 'zoology', 'botany', 'mathematics', 'computer', 'forestry'] else 'arts'
            dept = Department.objects.create(
                name=dept_name,
                slug=slug,
                category=category,
                order=60
            )
            dept_dict[dept_key] = dept
            print(f"Created Department on-the-fly: {dept_name}")

        # Create Faculty member
        faculty_member = DepartmentFaculty.objects.create(
            department=dept,
            name=name,
            designation=post,
            order=order
        )
        imported_count += 1

    print(f"Successfully imported {imported_count} faculty members!")

if __name__ == '__main__':
    run()
