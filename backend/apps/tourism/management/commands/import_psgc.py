import csv
from django.core.management.base import BaseCommand
from apps.tourism.models import Province, CityMunicipality

class Command(BaseCommand):
    help = "Import PSGC data from CSV"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to the PSGC CSV file")

    def handle(self, **kwargs):
        csv_file = kwargs["csv_file"]

        try:
            with open(csv_file, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for row in reader:
                    psgc_code = row.get("psgc_code")
                    name = row.get("name")
                    province_name = row.get("province_name")

                    if row.get("level") == "Province":
                        province, created = Province.objects.get_or_create(
                            psgc_code=psgc_code,
                            defaults={"name": name},
                        )
                        if created:
                            self.stdout.write(self.style.SUCCESS(f"Added province {name}"))

                    elif row.get("level") == "City/Municipality":
                        province, _ = Province.objects.get_or_create(name=province_name)
                        _, created = CityMunicipality.objects.get_or_create(
                            psgc_code=psgc_code,
                            province=province,
                            defaults={"name": name},
                        )
                        if created:
                            self.stdout.write(self.style.SUCCESS(f"Added city {name}"))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"File not found: {csv_file}"))
