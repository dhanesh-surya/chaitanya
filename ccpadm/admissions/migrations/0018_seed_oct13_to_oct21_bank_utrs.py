# Generated to seed additional PNB bank statement records (13-10-2026 to 21-10-2026)

from django.db import migrations


def seed_latest_bank_utrs(apps, schema_editor):
    BankStatementUTR = apps.get_model('admissions', 'BankStatementUTR')
    from admissions.bank_statement_seed_data import BANK_STATEMENT_SEED_RECORDS

    existing = set(BankStatementUTR.objects.values_list('utr_no', flat=True))
    objs = []
    for item in BANK_STATEMENT_SEED_RECORDS:
        utr = item['utr_no'].strip()
        if utr and utr not in existing:
            existing.add(utr)
            objs.append(
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
    if objs:
        BankStatementUTR.objects.bulk_create(objs, ignore_conflicts=True)


class Migration(migrations.Migration):

    dependencies = [
        ('admissions', '0017_seed_additional_bank_utrs'),
    ]

    operations = [
        migrations.RunPython(seed_latest_bank_utrs, migrations.RunPython.noop),
    ]
