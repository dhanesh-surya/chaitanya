import re
from collections import defaultdict
from django.db import OperationalError, ProgrammingError


def ensure_bank_utrs_seeded():
    """Ensure the pre-loaded PNB bank statement UTRs are present in the database."""
    from admissions.models import BankStatementUTR
    from admissions.bank_statement_seed_data import BANK_STATEMENT_SEED_RECORDS

    try:
        existing_count = BankStatementUTR.objects.count()
        if existing_count >= len(BANK_STATEMENT_SEED_RECORDS):
            return existing_count

        existing_utrs = set(BankStatementUTR.objects.values_list('utr_no', flat=True))
        to_create = []
        for item in BANK_STATEMENT_SEED_RECORDS:
            utr = item['utr_no'].strip()
            if utr and utr not in existing_utrs:
                existing_utrs.add(utr)
                to_create.append(
                    BankStatementUTR(
                        utr_no=utr,
                        tran_date=item.get('tran_date', ''),
                        amount=item.get('amount', '500.00'),
                        sender_name=item.get('sender_name', ''),
                        bank_code=item.get('bank_code', ''),
                        upi_id=item.get('upi_id', ''),
                        narration=item.get('narration', ''),
                        statement_source=item.get('statement_source', 'PNB Bank Statement'),
                    )
                )
        if to_create:
            BankStatementUTR.objects.bulk_create(to_create, ignore_conflicts=True)
        return BankStatementUTR.objects.count()
    except (OperationalError, ProgrammingError):
        return 0


def normalize_student_utr(raw_utr):
    """
    Smartly normalize a UTR / Transaction ID entered by a student.
    Handles formats like:
    - '491984771896'
    - '4919 8477 1896'
    - 'UPI/CR/491984771896/MUKESH/...'
    - 'UTR: 491984771896' or 'UTR No - 491984771896'
    """
    if not raw_utr:
        return ''
    s = str(raw_utr).strip()

    # 1. Check if student pasted full UPI/CR/<digits> narration
    upi_match = re.search(r'UPI/CR/(\d{8,18})', s, flags=re.IGNORECASE)
    if upi_match:
        return upi_match.group(1)

    # 2. Check if NEFT UTR format (e.g. YESF262816201367)
    neft_match = re.search(r'\b([A-Z]{4}\d{10,16})\b', s.upper())
    if neft_match:
        return neft_match.group(1)

    # 3. Check for a continuous 10 to 16 digit number (after removing spaces/hyphens)
    compact = re.sub(r'[\s\-]+', '', s)
    digit_match = re.search(r'(\d{10,16})', compact)
    if digit_match:
        return digit_match.group(1)

    # 4. Fallback: strip common prefixes and non-alphanumerics
    cleaned = re.sub(r'^(UTR|TXN|REF|NO|ID|NUMBER)[:\-\s#]*', '', s, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r'[^A-Za-z0-9]', '', cleaned).upper()
    return cleaned


def parse_bank_statement_text(text, source_name='Uploaded Statement'):
    """
    Extract UTR records from bank statement text (PNB Narration column, IMPS/NEFT, or raw UTR list).
    Handles line-wraps/spaces inside PDF table cells and always catches standalone 12-digit UTRs.
    """
    if not text:
        return []

    records = []
    seen_utrs = set()

    # Pre-normalize PDF line breaks inside "UPI/CR/<digits>" where pypdf wraps numbers across lines
    normalized_text = re.sub(
        r'(UPI\s*[/\-]\s*(?:CR|DR)\s*[/\-]\s*\d{4,11})\s*\n\s*(\d{1,10})',
        r'\1\2',
        text,
        flags=re.IGNORECASE,
    )

    # 1. Match PNB UPI/CR/<UTR>/<Name>/<Bank>/<UPI_ID> format (allowing optional whitespace around slashes)
    upi_pattern = re.compile(
        r'UPI\s*[/\-]\s*(?:CR|DR)\s*[/\-]\s*(\d{8,18})(?:\s*/\s*([^/\n\r]*))?(?:\s*/\s*([^/\n\r]*))?(?:\s*/\s*([^\s\n\r]*))?',
        flags=re.IGNORECASE,
    )
    for m in upi_pattern.finditer(normalized_text):
        utr = m.group(1).strip()
        if utr in seen_utrs:
            continue
        seen_utrs.add(utr)

        sender = (m.group(2) or '').strip()
        bank = (m.group(3) or '').strip()
        rest = (m.group(4) or '').strip()

        date_m = re.search(r'(\d{2}[/\-]\d{2}[/\-]\d{4})$', rest)
        tran_date = ''
        if date_m:
            tran_date = date_m.group(1).replace('/', '-')
            rest = rest[:-10].strip()
        else:
            window = normalized_text[max(0, m.start() - 60):min(len(normalized_text), m.end() + 40)]
            dm = re.search(r'(\d{2}[/\-]\d{2}[/\-]\d{4})', window)
            if dm:
                tran_date = dm.group(1).replace('/', '-')

        upi_id = rest.split('/')[0] if '/' in rest else rest
        narration = f'UPI/CR/{utr}/{sender}/{bank}/{rest}'.rstrip('/')

        records.append({
            'utr_no': utr,
            'tran_date': tran_date,
            'amount': '500.00',
            'sender_name': sender[:150],
            'bank_code': bank[:50],
            'upi_id': upi_id[:150],
            'narration': narration[:500],
            'statement_source': source_name[:200],
        })

    # 2. Match IMPS / generic UPI patterns (e.g. IMPS/P2A/<UTR>/<Sender> or UPI/<UTR>/...)
    imps_pattern = re.compile(
        r'(?:IMPS\s*[/\-]\s*(?:P2A|P2M|IN|CR)?\s*[/\-]?|UPI\s*[/\-])\s*(\d{10,16})(?:\s*/\s*([^/\n\r]*))?',
        flags=re.IGNORECASE,
    )
    for m in imps_pattern.finditer(normalized_text):
        utr = m.group(1).strip()
        if utr in seen_utrs:
            continue
        seen_utrs.add(utr)
        sender = (m.group(2) or '').strip()
        window = normalized_text[max(0, m.start() - 60):min(len(normalized_text), m.end() + 40)]
        dm = re.search(r'(\d{2}[/\-]\d{2}[/\-]\d{4})', window)
        tran_date = dm.group(1).replace('/', '-') if dm else ''
        records.append({
            'utr_no': utr,
            'tran_date': tran_date,
            'amount': '500.00',
            'sender_name': sender[:150],
            'bank_code': '',
            'upi_id': '',
            'narration': m.group(0).strip()[:500],
            'statement_source': source_name[:200],
        })

    # 3. Match NEFT / RTGS IN::<UTR>/<Sender> format
    for m in re.finditer(r'(?:NEFT|RTGS)[\s:_\-/]*(?:IN)?[\s:_\-/]*([A-Z]{4}[A-Z0-9]{8,18})(?:/([^/\n\r]*))?', normalized_text, flags=re.IGNORECASE):
        utr = m.group(1).strip().upper()
        if utr in seen_utrs:
            continue
        seen_utrs.add(utr)
        sender = (m.group(2) or '').strip()
        window = normalized_text[max(0, m.start() - 60):min(len(normalized_text), m.end() + 40)]
        dm = re.search(r'(\d{2}[/\-]\d{2}[/\-]\d{4})', window)
        tran_date = dm.group(1).replace('/', '-') if dm else ''
        records.append({
            'utr_no': utr,
            'tran_date': tran_date,
            'amount': '500.00',
            'sender_name': sender[:150],
            'bank_code': utr[:4],
            'upi_id': '',
            'narration': m.group(0).strip()[:500],
            'statement_source': source_name[:200],
        })

    # 4. Always scan for any remaining 12-digit UTR numbers in the text that weren't caught above
    # (Skip common 16-digit account numbers because \b\d{12}\b only matches exact 12-digit tokens)
    for m in re.finditer(r'\b(\d{12})\b', normalized_text):
        utr = m.group(1)
        if utr not in seen_utrs:
            seen_utrs.add(utr)
            window = normalized_text[max(0, m.start() - 60):min(len(normalized_text), m.end() + 60)]
            dm = re.search(r'(\d{2}[/\-]\d{2}[/\-]\d{4})', window)
            tran_date = dm.group(1).replace('/', '-') if dm else ''
            records.append({
                'utr_no': utr,
                'tran_date': tran_date,
                'amount': '500.00',
                'sender_name': '',
                'bank_code': '',
                'upi_id': '',
                'narration': f'UTR/{utr}',
                'statement_source': source_name[:200],
            })

    return records


def import_bank_statement_records(records):
    """
    Save parsed bank statement UTR records into the database.
    Safe to run repeatedly on the same statement:
    - Existing UTRs are never duplicated.
    - If an existing UTR had missing sender_name/tran_date and the re-upload has them, it updates them.
    Returns (total_parsed, newly_added).
    """
    from admissions.models import BankStatementUTR

    if not records:
        return 0, 0

    ensure_bank_utrs_seeded()
    existing_objs = {obj.utr_no: obj for obj in BankStatementUTR.objects.all()}
    to_create = []
    to_update = []

    for item in records:
        utr = (item.get('utr_no') or '').strip()
        if not utr:
            continue
        if utr not in existing_objs:
            new_obj = BankStatementUTR(
                utr_no=utr,
                tran_date=item.get('tran_date', ''),
                amount=item.get('amount', '500.00'),
                sender_name=item.get('sender_name', ''),
                bank_code=item.get('bank_code', ''),
                upi_id=item.get('upi_id', ''),
                narration=item.get('narration', ''),
                statement_source=item.get('statement_source', 'Uploaded Statement'),
            )
            existing_objs[utr] = new_obj
            to_create.append(new_obj)
        else:
            # Enrich existing record if it was missing sender_name or tran_date
            obj = existing_objs[utr]
            changed = False
            if not obj.sender_name and item.get('sender_name'):
                obj.sender_name = item['sender_name']
                changed = True
            if not obj.tran_date and item.get('tran_date'):
                obj.tran_date = item['tran_date']
                changed = True
            if (not obj.narration or obj.narration.startswith('UTR/')) and item.get('narration') and not item['narration'].startswith('UTR/'):
                obj.narration = item['narration']
                changed = True
            if changed and obj.pk:
                to_update.append(obj)

    if to_create:
        BankStatementUTR.objects.bulk_create(to_create, ignore_conflicts=True)
    if to_update:
        BankStatementUTR.objects.bulk_update(to_update, ['sender_name', 'tran_date', 'narration'])
    return len(records), len(to_create)


def parse_and_import_bank_pdf(pdf_file, filename='Bank_Statement.pdf'):
    """Read a PDF file, extract all UPI/CR, IMPS, NEFT & 12-digit UTRs, and store in BankStatementUTR."""
    import pypdf

    reader = pypdf.PdfReader(pdf_file)
    full_text = '\n'.join((page.extract_text() or '') for page in reader.pages)
    records = parse_bank_statement_text(full_text, source_name=filename)
    return import_bank_statement_records(records)


def parse_and_import_bank_excel(excel_file, filename='Bank_Statement.xlsx'):
    """Read an Excel (.xlsx) bank statement, extract all UTRs from all sheets/rows, and store in BankStatementUTR."""
    import openpyxl

    wb = openpyxl.load_workbook(excel_file, data_only=True)
    lines = []
    for sheet in wb.worksheets:
        for row in sheet.iter_rows(values_only=True):
            row_str = ' '.join(str(cell).strip() for cell in row if cell is not None and str(cell).strip())
            if row_str:
                lines.append(row_str)
    full_text = '\n'.join(lines)
    records = parse_bank_statement_text(full_text, source_name=filename)
    return import_bank_statement_records(records)


def get_bank_utr_lookup():
    """
    Returns (exact_map, stripped_zero_map, total_bank_utrs) for fast in-memory verification.
    """
    from admissions.models import BankStatementUTR

    ensure_bank_utrs_seeded()
    exact_map = {}
    stripped_map = {}
    try:
        for rec in BankStatementUTR.objects.all():
            key = rec.utr_no.strip().upper()
            exact_map[key] = rec
            stripped = key.lstrip('0')
            if stripped and len(stripped) >= 8:
                stripped_map[stripped] = rec
    except (OperationalError, ProgrammingError):
        pass
    return exact_map, stripped_map, len(exact_map)


def match_utr_against_bank(raw_utr, exact_map, stripped_map):
    """
    Matches a student's raw transaction_id against the bank lookup maps.
    Returns (clean_utr, matched_BankStatementUTR_or_None).
    """
    clean = normalize_student_utr(raw_utr)
    if not clean:
        return '', None

    upper_clean = clean.upper()
    if upper_clean in exact_map:
        return clean, exact_map[upper_clean]

    # Check zero-padded 12-digit match (e.g., '5650370822' -> '005650370822')
    if upper_clean.isdigit() and len(upper_clean) < 12:
        padded = upper_clean.zfill(12)
        if padded in exact_map:
            return clean, exact_map[padded]

    # Check stripped leading zeros match
    stripped = upper_clean.lstrip('0')
    if stripped and len(stripped) >= 8 and stripped in stripped_map:
        return clean, stripped_map[stripped]

    return clean, None


def attach_utr_verification(enrollment_list):
    """
    Annotates a list of StudentEnrollment or NepUgAdmissionEnrollment objects in-place with:
    - e.clean_utr
    - e.utr_verified (bool)
    - e.bank_utr_record (BankStatementUTR or None)
    - e.utr_is_duplicate (bool)
    - e.utr_duplicate_count (int)
    - e.utr_duplicate_info (str)
    Returns summary dict: {
        'verified_count': int,
        'unverified_count': int,
        'duplicate_count': int,
        'bank_utr_total': int,
    }
    """
    from admissions.models import StudentEnrollment, NepUgAdmissionEnrollment

    exact_map, stripped_map, bank_utr_total = get_bank_utr_lookup()

    # Build global usage map across all enrollments to detect duplicate UTR usage
    utr_usage = defaultdict(list)
    try:
        for reg_no, full_name, tx_id in StudentEnrollment.objects.exclude(transaction_id='').values_list('reg_no', 'full_name', 'transaction_id'):
            c = normalize_student_utr(tx_id)
            if c:
                utr_usage[c.lstrip('0').upper() or c.upper()].append(f'{full_name} ({reg_no})')
        for reg_no, full_name, tx_id in NepUgAdmissionEnrollment.objects.exclude(transaction_id='').values_list('reg_no', 'full_name', 'transaction_id'):
            c = normalize_student_utr(tx_id)
            if c:
                label = f'{full_name} ({reg_no} - NEP)'
                key = c.lstrip('0').upper() or c.upper()
                if not any(reg_no in existing for existing in utr_usage[key]):
                    utr_usage[key].append(label)
    except (OperationalError, ProgrammingError):
        pass

    verified_count = 0
    unverified_count = 0
    duplicate_count = 0

    for e in enrollment_list:
        raw_tx = (getattr(e, 'transaction_id', '') or '').strip()
        clean_utr, bank_rec = match_utr_against_bank(raw_tx, exact_map, stripped_map)
        e.clean_utr = clean_utr
        e.bank_utr_record = bank_rec
        e.utr_verified = bank_rec is not None

        usage_key = clean_utr.lstrip('0').upper() or clean_utr.upper() if clean_utr else ''
        users = utr_usage.get(usage_key, []) if usage_key else []
        e.utr_duplicate_count = len(users)
        e.utr_is_duplicate = len(users) > 1
        e.utr_duplicate_info = ', '.join(users) if len(users) > 1 else ''

        if raw_tx:
            if e.utr_verified:
                verified_count += 1
            else:
                unverified_count += 1
            if e.utr_is_duplicate:
                duplicate_count += 1

    return {
        'verified_count': verified_count,
        'unverified_count': unverified_count,
        'duplicate_count': duplicate_count,
        'bank_utr_total': bank_utr_total,
    }
