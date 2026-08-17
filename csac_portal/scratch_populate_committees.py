import os
import django
import html.parser
from django.utils.text import slugify

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_portal.settings')
django.setup()

from core.models import Committee, CommitteeMember

class CommitteeHTMLParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.current_cell_text = []
        self.current_row = []
        self.rows = []

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            # Check if this is the committees table
            self.in_table = True
        elif tag == 'tr' and self.in_table:
            self.in_row = True
            self.current_row = []
        elif tag in ['td', 'th'] and self.in_row:
            self.in_cell = True
            self.current_cell_text = []
        elif tag == 'br' and self.in_cell:
            self.current_cell_text.append('\n')

    def handle_endtag(self, tag):
        if tag == 'table':
            self.in_table = False
        elif tag == 'tr' and self.in_row:
            self.in_row = False
            if self.current_row:
                self.rows.append(self.current_row)
        elif tag in ['td', 'th'] and self.in_cell:
            self.in_cell = False
            self.current_row.append("".join(self.current_cell_text).strip())

    def handle_data(self, data):
        if self.in_cell:
            self.current_cell_text.append(data)

def run():
    print("Starting committees populate script...")
    file_path = "C:/temp-csac/chaitanyacg.ac.in/committees.html"
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    parser = CommitteeHTMLParser()
    with open(file_path, 'r', encoding='utf-8') as f:
        parser.feed(f.read())

    # Find the committees table rows (we skip the header row)
    # The header row should be the first one containing 'Committee Name'
    header_index = -1
    for idx, r in enumerate(parser.rows):
        if len(r) > 1 and any('Committee Name' in col for col in r):
            header_index = idx
            break

    if header_index == -1:
        print("Error: Could not find committees table header in HTML.")
        return

    data_rows = parser.rows[header_index+1:]
    print(f"Found {len(data_rows)} committee rows to import.")

    # Clear existing committee members and committees to avoid duplicates
    CommitteeMember.objects.all().delete()
    Committee.objects.all().delete()
    print("Cleared existing Committee and CommitteeMember records.")

    imported_count = 0
    for idx, row in enumerate(data_rows):
        # We expect 4 columns: Sr. No., Committee Name, Coordinator/Members, Positions
        if len(row) < 4:
            continue

        sno_str, name, members_str, positions_str = row
        sno_str = sno_str.strip()
        name = name.strip()
        
        if not name:
            continue

        try:
            order = int(sno_str)
        except ValueError:
            order = idx + 1

        # Generate unique slug
        slug = slugify(name)
        if not slug:
            slug = f"committee-{order}"

        # Create Committee
        committee = Committee.objects.create(
            name=name,
            slug=slug,
            description=f"Official {name} of Chaitanya Science and Arts College.",
            order=order
        )

        # Parse members and positions
        members = [m.strip() for m in members_str.split('\n') if m.strip()]
        positions = [p.strip() for p in positions_str.split('\n') if p.strip()]

        # Pair members and positions
        max_len = max(len(members), len(positions))
        for m_idx in range(max_len):
            m_name = members[m_idx] if m_idx < len(members) else "Unknown"
            m_pos = positions[m_idx] if m_idx < len(positions) else "Member"

            # Determine role in committee (like Coordinator, Member)
            role = m_pos
            
            CommitteeMember.objects.create(
                committee=committee,
                name=m_name,
                designation="Faculty Member",  # Default designation
                role_in_committee=role,
                order=m_idx + 1
            )

        print(f"Imported Committee: {name} with {max_len} members.")
        imported_count += 1

    print(f"Successfully imported {imported_count} committees!")

if __name__ == '__main__':
    run()
