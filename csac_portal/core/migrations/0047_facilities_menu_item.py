from django.db import migrations


def create_facilities_menu_item(apps, schema_editor):
    MenuItem = apps.get_model('core', 'MenuItem')

    MenuItem.objects.get_or_create(
        title='Facilities',
        parent=None,
        defaults={
            'url': 'core:infrastructure',
            'is_named_url': True,
            'open_in_new_tab': False,
            'order': 6,
            'is_active': True,
        },
    )


def remove_facilities_menu_item(apps, schema_editor):
    MenuItem = apps.get_model('core', 'MenuItem')
    MenuItem.objects.filter(title='Facilities', parent=None).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0046_infrastructureimage_description'),
    ]

    operations = [
        migrations.RunPython(create_facilities_menu_item, remove_facilities_menu_item),
    ]