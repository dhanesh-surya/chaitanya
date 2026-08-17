from django.db import migrations


def fix_program_type_codes(apps, schema_editor):
    Program = apps.get_model('academics', 'Program')
    ProgramType = apps.get_model('academics', 'ProgramType')

    for program_type in ProgramType.objects.all():
        Program.objects.filter(program_type=program_type.name).update(program_type=program_type.code)

    legacy_map = {
        'Undergraduate': 'ug',
        'Postgraduate': 'pg',
        'Diploma': 'diploma',
        'Certificate': 'cert',
    }
    for old_value, code in legacy_map.items():
        Program.objects.filter(program_type=old_value).update(program_type=code)


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0006_program_type_and_duration_text'),
    ]

    operations = [
        migrations.RunPython(fix_program_type_codes, migrations.RunPython.noop),
    ]