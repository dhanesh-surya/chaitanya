import os
import sys
import django
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_portal.settings')
django.setup()

from academics.models import Department, Program

# Path to the programs/index.html file
html_path = "C:/temp-csac/chaitanyacg.ac.in/programs/index.html"

with open(html_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

table = soup.find('table')
rows = table.find('tbody').find_all('tr')

print(f"Found {len(rows)} programs in the table.")

# Department mappings (by keywords or slug)
dept_keywords = {
    'Forestry': 'forestry',
    'B.Com': 'commerce-management',
    'M.Com': 'commerce-management',
    'Commerce': 'commerce-management',
    'B.C.A': 'computer-science',
    'DCA': 'computer-science',
    'PGDCA': 'computer-science',
    'B.B.A': 'commerce-management',
    'MSW': 'social-work',
    'English': 'english',
    'Political Science': 'political-science',
    'Maths': 'mathematics',
    'Physics': 'physics',
}

# If multiple departments are involved or it's general, we map to None
def get_department(name):
    # Special cases for mixed/cross-department programs
    if any(keyword in name for keyword in ['Hindi, Sociology, Geography', 'Computer Science, Chemistry', 'Botany, Zoology', 'FC, Political Science, History', 'FC, Chemistry, Botany', 'FC, Physics, Chemistry']):
        return None
    for kw, slug in dept_keywords.items():
        if kw in name:
            try:
                return Department.objects.get(slug=slug)
            except Department.DoesNotExist:
                print(f"Department with slug '{slug}' does not exist.")
    return None

def get_program_type(name):
    name_upper = name.upper()
    if 'DCA' in name_upper: # includes DCA, PGDCA
        return 'diploma'
    elif name_upper.startswith('B.'):
        return 'ug'
    elif name_upper.startswith('M.'):
        return 'pg'
    elif 'MSW' in name_upper:
        return 'pg'
    return 'ug'

def get_duration(duration_text):
    duration_text = duration_text.lower()
    if '3' in duration_text or 'three' in duration_text:
        return '3'
    elif '2' in duration_text or 'two' in duration_text:
        return '2'
    elif '1' in duration_text or 'one' in duration_text:
        return '1'
    return '3' # fallback

# Clear existing programs to re-seed fresh, keeping ordering exactly as in table
Program.objects.all().delete()

for idx, row in enumerate(rows):
    cols = [col.text.strip() for col in row.find_all('td')]
    if len(cols) < 6:
        continue
    
    sr_no = cols[0]
    name = cols[1]
    introduced = cols[2]
    duration_str = cols[3]
    seats = cols[4]
    affiliation = cols[5]
    
    dept = get_department(name)
    prog_type = get_program_type(name)
    duration = get_duration(duration_str)
    
    try:
        introduced_year = int(introduced)
    except ValueError:
        introduced_year = None
        
    program = Program.objects.create(
        name=name,
        department=dept,
        program_type=prog_type,
        duration=duration,
        seats=seats,
        introduced_year=introduced_year,
        affiliation_status=affiliation,
        order=idx * 10
    )
    print(f"Created: {program.name} ({program.get_program_type_display()}), Year: {program.introduced_year}, Seats: {program.seats}, Dept: {program.department}")

print("Seeding completed successfully!")
