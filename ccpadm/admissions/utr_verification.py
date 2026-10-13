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
    Extract UTR records from bank statement text (PNB Narration column or raw UTR list).
    """
    if not text:
        return []

    records = []
    seen_utrs = set()

    # 1. Match PNB UPI/CR/<UTR>/<Name>/<Bank>/<UPI_ID> format
    for m in re.finditer(r'UPI/CR/(\d{8,18})(?:/([^/\n\r]*))?(?:/([^/\n\r]*))?(?:/([^\s\n\r]*))?', text, flags=re.IGNORECASE):
        utr = m.group(1).strip()
        if utr in seen_utrs:
            continue
        seen_utrs.add(utr)

        sender = (m.group(2) or '').strip()
        bank = (m.group(3) or '').strip()
        rest = (m.group(4) or '').strip()

        date_m = re.search(r'(\d{2}-\d{2}-\d{4})$', rest)
        tran_date = ''
        if date_m:
            tran_date = date_m.group(1)
            rest = rest[:-10].strip()
        else:
            window = text[max(0, m.start() - 50):min(len(text), m.end() + 30)]
            dm = re.search(r'(\d{2}-\d{2}-\d{4})', window)
            if dm:
                tran_date = dm.group(1)

        upi_id = rest.split('/')[0] if '/' in rest else rest
        narration = f'UPI/CR/{utr}/{sender}/{bank}/{rest}'.rstrip('/')

        records.append({
            'utr_no': utr,
            'tran_date': tran_date,
            'amount': '500.00',
            'sender_name': sender,
            'bank_code': bank,
            'upi_id': upi_id,
            'narration': narration[:500],
            'statement_source': source_name[:200],
        })

    # 2. Match NEFT IN::<UTR>/<Sender> format
    for m in re.finditer(r'NEFT\s+IN::([A-Z0-9]{10,22})(?:/([^/\n\r]*))?', text, flags=re.IGNORECASE):
        utr = m.group(1).strip().upper()
        if utr in seen_utrs:
            continue
        seen_utrs.add(utr)
        sender = (m.group(2) or '').strip()
        window = text[max(0, m.start() - 50):min(len(text), m.end() + 40)]
        dm = re.search(r'(\d{2}-\d{2}-\d{4})', window)
        tran_date = dm.group(1) if dm else ''
        records.append({
            'utr_no': utr,
            'tran_date': tran_date,
            'amount': '500.00',
            'sender_name': sender[:150],
            'bank_code': utr[:4],
            'upi_id': '',
            'narration': m.group(0)[:500],
            'statement_source': source_name[:200],
        })

    # 3. If no UPI/CR or NEFT patterns found, check if user pasted/uploaded raw 12-digit UTR numbers
    if not records:
        for m in re.finditer(r'\b(\d{12})\b', text):
            utr = m.group(1)
            if utr not in seen_utrs:
                seen_utrs.add(utr)
                records.append({
                    'utr_no': utr,
                    'tran_date': '',
                    'amount': '500.00',
                    'sender_name': '',
                    'bank_code': '',
                    'upi_id': '',
                    'narration': f'UPI/CR/{utr}',
                    'statement_source': source_name[:200],
                })

    return records


def import_bank_statement_records(records):
    """Save parsed bank statement UTR records into the database. Returns (total_parsed, newly_added)."""
    from admissions.models import BankStatementUTR

    if not records:
        return 0, 0

    ensure_bank_utrs_seeded()
    existing_utrs = set(BankStatementUTR.objects.values_list('utr_no', flat=True))
    to_create = []
    for item in records:
        utr = (item.get('utr_no') or '').strip()
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
                    statement_source=item.get('statement_source', 'Uploaded Statement'),
                )
            )
    if to_create:
        BankStatementUTR.objects.bulk_create(to_create, ignore_conflicts=True)
    return len(records), len(to_create)


def parse_and_import_bank_pdf(pdf_file, filename='Bank_Statement.pdf'):
    """Read a PDF file, extract all UPI/CR & NEFT UTRs, and store in BankStatementUTR."""
    import pypdf

    reader = pypdf.PdfReader(pdf_file)
    full_text = '\n'.join((page.extract_text() or '') for page in reader.pages)
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
