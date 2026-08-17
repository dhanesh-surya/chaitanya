import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_portal.settings')
django.setup()

from core.models import QuickLinkCard

icons = {
    1: 'fa-graduation-cap',
    2: 'fa-building-columns',
    3: 'fa-book-bookmark',
    4: 'fa-calendar-days',
    5: 'fa-chalkboard-user',
    6: 'fa-lightbulb',
    7: 'fa-briefcase',
    8: 'fa-users-line',
    9: 'fa-trophy'
}

for card_id, icon_name in icons.items():
    try:
        card = QuickLinkCard.objects.get(id=card_id)
        card.fa_icon = icon_name
        card.save()
        print(f"Updated card {card.id} ({card.title}) with icon: {icon_name}")
    except Exception as e:
        print(f"Error on card {card_id}: {e}")
print("Done!")
