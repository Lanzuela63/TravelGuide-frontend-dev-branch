from django.core.management.base import BaseCommand
from apps.tourism.models import Province, CityMunicipality, TouristSpot, Hotel, Restaurant


class Command(BaseCommand):
    help = "Seed initial data for Bicol provinces, cities, and sample spots"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Seeding data..."))

        # Provinces
        provinces = [
            ("050000000", "Albay"),
            ("051600000", "Camarines Norte"),
            ("051700000", "Camarines Sur"),
            ("052000000", "Catanduanes"),
            ("054100000", "Masbate"),
            ("056200000", "Sorsogon"),
        ]

        province_objs = {}
        for psgc, name in provinces:
            province, _ = Province.objects.get_or_create(psgc_code=psgc, defaults={"name": name})
            province_objs[name] = province

        # Cities / Municipalities
        cities = [
            # Albay
            ("Legazpi City", "050500000", "Albay"),
            ("Daraga", "050503000", "Albay"),

            # Camarines Norte
            ("Daet", "051601000", "Camarines Norte"),

            # Camarines Sur
            ("Naga City", "051711000", "Camarines Sur"),
            ("Caramoan", "051706000", "Camarines Sur"),

            # Catanduanes
            ("Virac", "052007000", "Catanduanes"),

            # Masbate
            ("Masbate City", "054107000", "Masbate"),

            # Sorsogon
            ("Sorsogon City", "056202000", "Sorsogon"),
        ]

        city_objs = {}
        for name, psgc, prov_name in cities:
            city, _ = CityMunicipality.objects.get_or_create(
                psgc_code=psgc,
                province=province_objs[prov_name],
                defaults={"name": name}
            )
            city_objs[name] = city

        # Tourist Spots
        TouristSpot.objects.get_or_create(
            name="Mayon Volcano",
            city=city_objs["Legazpi City"],
            defaults={
                "description": "A perfect cone-shaped volcano and iconic landmark of the Philippines.",
                "email": "info@mayon.com",
                "website": "https://tourism.albay.gov.ph/mayon",
                "is_featured": True,
                "show_in_carousel": True,
            }
        )

        TouristSpot.objects.get_or_create(
            name="Caramoan Islands",
            city=city_objs["Caramoan"],
            defaults={
                "description": "Famous for pristine beaches and as a Survivor TV show location.",
                "email": "info@caramoanislands.com",
                "website": "https://caramoanislands.com",
                "is_featured": True,
            }
        )

        # Hotels
        Hotel.objects.get_or_create(
            name="Hotel St. Ellis",
            city=city_objs["Legazpi City"],
            defaults={
                "description": "A modern hotel near Mayon Volcano with amenities and services.",
                "stars": 4,
            }
        )

        # Restaurants
        Restaurant.objects.get_or_create(
            name="Small Talk Cafe",
            city=city_objs["Legazpi City"],
            defaults={
                "description": "Famous for their pinangat pasta and local Bicolano cuisine.",
                "cuisine_type": "Filipino",
            }
        )

        self.stdout.write(self.style.SUCCESS("✅ Seeding complete!"))
