import io
import csv
import openpyxl
from django.db import transaction
from library.models import (
    Book, BookCopy, Publisher, Subject, BookCategory, ExcelImport, AuditLog
)
from academics.models import Department


HEADER_ALIASES = {
    'accession_number': ['accession no', 'accession number', 'acc no', 'acc_no', 'accno', 'accession', 'barcode'],
    'title': ['title', 'book title', 'book_title', 'name of book', 'book name'],
    'author': ['author', 'authors', 'author name', 'writer'],
    'publisher': ['publisher', 'publishing house', 'publication'],
    'edition': ['edition', 'ed'],
    'publication_year': ['year', 'publication year', 'pub year', 'year of publication'],
    'subject': ['subject', 'sub', 'subject name'],
    'category': ['category', 'type', 'book type'],
    'department': ['department', 'dept'],
    'rack_location': ['rack', 'shelf', 'rack location', 'location', 'almirah'],
    'price': ['price', 'cost', 'amount', 'mrp'],
    'isbn': ['isbn', 'isbn number'],
    'pages': ['pages', 'page count', 'no of pages'],
    'language': ['language', 'lang'],
}


def normalize_header(header_text):
    if not header_text:
        return ''
    cleaned = str(header_text).strip().lower().replace('_', ' ').replace('.', '')
    for canon_key, aliases in HEADER_ALIASES.items():
        if cleaned == canon_key or cleaned in aliases:
            return canon_key
    return cleaned


def parse_rows_from_file(uploaded_file):
    filename = uploaded_file.name.lower()
    raw_rows = []

    if filename.endswith('.csv'):
        content = uploaded_file.read().decode('utf-8', errors='ignore')
        reader = csv.reader(io.StringIO(content))
        raw_rows = [row for row in reader if any(cell.strip() for cell in row)]
    elif filename.endswith(('.xlsx', '.xls')):
        wb = openpyxl.load_workbook(uploaded_file, data_only=True)
        sheet = wb.active
        for row in sheet.iter_rows(values_only=True):
            if any(cell is not None and str(cell).strip() for cell in row):
                raw_rows.append([str(c).strip() if c is not None else '' for c in row])
    else:
        raise ValueError("Unsupported file format. Please upload an Excel (.xlsx, .xls) or CSV (.csv) file.")

    if not raw_rows or len(raw_rows) < 2:
        raise ValueError("Uploaded file appears to be empty or missing data rows.")

    headers = [normalize_header(col) for col in raw_rows[0]]
    data_rows = []
    for row_idx, row_data in enumerate(raw_rows[1:], start=2):
        row_dict = {}
        for col_idx, key in enumerate(headers):
            if key and col_idx < len(row_data):
                row_dict[key] = str(row_data[col_idx]).strip()
        row_dict['_row_num'] = row_idx
        data_rows.append(row_dict)

    return headers, data_rows


def validate_import_data(data_rows):
    existing_accessions = set(BookCopy.objects.values_list('accession_number', flat=True))
    seen_in_file = set()

    valid_rows = []
    error_rows = []

    for row in data_rows:
        row_num = row.get('_row_num', 0)
        acc_no = row.get('accession_number', '').strip()
        title = row.get('title', '').strip()
        author = row.get('author', '').strip()

        errors = []
        if not acc_no:
            errors.append("Missing Accession Number")
        elif acc_no in existing_accessions:
            errors.append(f"Accession number '{acc_no}' already exists in library inventory")
        elif acc_no in seen_in_file:
            errors.append(f"Duplicate Accession number '{acc_no}' within uploaded file")
        else:
            seen_in_file.add(acc_no)

        if not title:
            errors.append("Missing Book Title")
        if not author:
            errors.append("Missing Author Name")

        if errors:
            error_rows.append({
                'row_num': row_num,
                'accession_number': acc_no,
                'title': title,
                'author': author,
                'reasons': "; ".join(errors)
            })
        else:
            valid_rows.append(row)

    return {
        'total_rows': len(data_rows),
        'valid_count': len(valid_rows),
        'error_count': len(error_rows),
        'valid_rows': valid_rows,
        'error_rows': error_rows,
    }


@transaction.atomic
def commit_import_records(valid_rows, uploaded_by_user=None, file_name="imported_file.xlsx", ip_address=None):
    # Caches to avoid duplicate DB hits
    publishers = {p.name.lower(): p for p in Publisher.objects.all()}
    subjects = {s.name.lower(): s for s in Subject.objects.all()}
    categories = {c.name.lower(): c for c in BookCategory.objects.all()}
    departments = {d.name.lower(): d for d in Department.objects.all()}

    books_by_key = {}
    for b in Book.objects.all():
        key = (b.title.strip().lower(), b.author.strip().lower())
        books_by_key[key] = b

    created_books_count = 0
    created_copies_count = 0

    copies_to_create = []

    for row in valid_rows:
        title = row.get('title', '').strip()
        author = row.get('author', '').strip()
        book_key = (title.lower(), author.lower())

        book = books_by_key.get(book_key)
        if not book:
            # Resolve Publisher
            pub_name = row.get('publisher', '').strip()
            pub_obj = None
            if pub_name:
                pub_lower = pub_name.lower()
                if pub_lower in publishers:
                    pub_obj = publishers[pub_lower]
                else:
                    pub_obj = Publisher.objects.create(name=pub_name)
                    publishers[pub_lower] = pub_obj

            # Resolve Subject
            sub_name = row.get('subject', '').strip()
            sub_obj = None
            if sub_name:
                sub_lower = sub_name.lower()
                if sub_lower in subjects:
                    sub_obj = subjects[sub_lower]
                else:
                    sub_obj = Subject.objects.create(name=sub_name)
                    subjects[sub_lower] = sub_obj

            # Resolve Category
            cat_name = row.get('category', '').strip()
            cat_obj = None
            if cat_name:
                cat_lower = cat_name.lower()
                if cat_lower in categories:
                    cat_obj = categories[cat_lower]
                else:
                    cat_obj = BookCategory.objects.create(name=cat_name)
                    categories[cat_lower] = cat_obj

            # Resolve Department
            dept_name = row.get('department', '').strip()
            dept_obj = None
            if dept_name:
                dept_lower = dept_name.lower()
                if dept_lower in departments:
                    dept_obj = departments[dept_lower]

            year_val = None
            if row.get('publication_year'):
                try:
                    year_val = int(row['publication_year'][:4])
                except (ValueError, TypeError):
                    year_val = None

            price_val = None
            if row.get('price'):
                try:
                    price_val = float(str(row['price']).replace('₹', '').replace(',', '').strip())
                except (ValueError, TypeError):
                    price_val = None

            book = Book.objects.create(
                title=title,
                author=author,
                isbn=row.get('isbn', '').strip(),
                publisher=pub_obj,
                edition=row.get('edition', '').strip(),
                publication_year=year_val,
                language=row.get('language', 'English').strip() or 'English',
                subject=sub_obj,
                category=cat_obj,
                department=dept_obj,
                price=price_val,
                is_active=True
            )
            books_by_key[book_key] = book
            created_books_count += 1

        acc_no = row.get('accession_number', '').strip()
        rack_loc = row.get('rack_location', '').strip()

        copy = BookCopy(
            book=book,
            accession_number=acc_no,
            rack_location=rack_loc,
            status='AVAILABLE',
            condition='GOOD',
            is_active=True
        )
        copies_to_create.append(copy)

    BookCopy.objects.bulk_create(copies_to_create)
    created_copies_count = len(copies_to_create)

    # Record ExcelImport summary
    imp = ExcelImport.objects.create(
        file_name=file_name,
        uploaded_by=uploaded_by_user,
        total_rows=len(valid_rows),
        valid_rows=created_copies_count,
        status='COMPLETED'
    )

    if uploaded_by_user:
        AuditLog.objects.create(
            user=uploaded_by_user,
            action='BOOK_IMPORTED',
            reference_id=str(imp.id),
            description=f"Imported {created_copies_count} copies ({created_books_count} new book titles) from {file_name}",
            ip_address=ip_address
        )

    return {
        'created_books': created_books_count,
        'created_copies': created_copies_count,
        'import_id': imp.id
    }
