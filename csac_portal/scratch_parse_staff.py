import html.parser

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
            cell_text = " ".join(self.current_cell_data).strip()
            self.current_row_cells.append(cell_text)

    def handle_data(self, data):
        if self.in_cell:
            self.current_cell_data.append(data.strip())

def parse_staff_html():
    file_path = "C:/temp-csac/chaitanyacg.ac.in/staff/1/index.html"
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    parser = StaffHTMLParser()
    parser.feed(html_content)
    
    print(f"Total rows found: {len(parser.rows)}")
    for i, row in enumerate(parser.rows[:15]):
        print(f"Row {i}: {row}")

if __name__ == '__main__':
    parse_staff_html()
