import json
from pathlib import Path

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


MODEL_LOAD_ORDER = [
    "academics.department",
    "academics.departmentbanner",
    "academics.departmentfaculty",
    "academics.departmentactivity",
    "academics.program",
    "academics.copomapping",
    "academics.syllabus",
    "academics.academiccalendar",
]


class Command(BaseCommand):
    help = "Upsert academics records from a JSON fixture without deleting other app data."

    def add_arguments(self, parser):
        parser.add_argument(
            "fixture",
            nargs="?",
            default="academics_data.json",
            help="Path to the academics JSON fixture.",
        )

    def handle(self, *args, **options):
        fixture_path = Path(options["fixture"])
        if not fixture_path.exists():
            raise CommandError(f"Fixture not found: {fixture_path}")

        with fixture_path.open(encoding="utf-8") as handle:
            payload = json.load(handle)

        grouped = {}
        for item in payload:
            grouped.setdefault(item["model"], []).append(item)

        created = 0
        updated = 0

        with transaction.atomic():
            for model_label in MODEL_LOAD_ORDER:
                for item in grouped.get(model_label, []):
                    model = apps.get_model(model_label)
                    fields = item["fields"].copy()
                    pk = item["pk"]

                    for field in model._meta.many_to_many:
                        fields.pop(field.name, None)

                    resolved_fields = {}
                    for name, value in fields.items():
                        field = model._meta.get_field(name)
                        if field.many_to_many:
                            continue
                        if field.is_relation and value is not None:
                            resolved_fields[name] = field.related_model.objects.get(pk=value)
                        else:
                            resolved_fields[name] = value

                    if model.objects.filter(pk=pk).exists():
                        instance = model.objects.get(pk=pk)
                        for name, value in resolved_fields.items():
                            setattr(instance, name, value)
                        instance.save()
                        updated += 1
                    else:
                        instance = model(pk=pk, **resolved_fields)
                        instance.save()
                        created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Academics sync complete: {created} created, {updated} updated."
            )
        )