# apps/tourism/management/commands/seed.py
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.tourism.models import Province, CityMunicipality, TouristSpot, Hotel, Restaurant


class Command(BaseCommand):
    help = "Seed the database with sample provinces, cities, tourist spots, hotels, and restaurants."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🌱 Starting database seed..."))

        # --- Provinces ---
        provinces = [
            {"psgc_code": "050500000", "name": "Albay"},
            {"psgc_code": "051600000", "name": "Camarines Norte"},
            {"psgc_code": "051700000", "name": "Camarines Sur"},
            {"psgc_code": "052000000", "name": "Catanduanes"},
            {"psgc_code": "054100000", "name": "Masbate"},
            {"psgc_code": "056200000", "name": "Sorsogon"},
        ]

        province_objs = {}
        for data in provinces:
            province, created = Province.objects.get_or_create(
                slug=slugify(data["name"]),
                defaults={
                    "psgc_code": data["psgc_code"],
                    "name": data["name"],
                },
            )
            province_objs[data["name"]] = province
            self.stdout.write(f"✅ Province: {province.name} ({'created' if created else 'exists'})")

        # --- Cities/Municipalities ---
        cities = {
            "Albay": ["Legazpi City", "Daraga"],
            "Camarines Norte": ["Daet"],
            "Camarines Sur": ["Naga City", "Caramoan"],
            "Catanduanes": ["Virac"],
            "Masbate": ["Masbate City"],
            "Sorsogon": ["Sorsogon City", "Donsol"],
        }

        city_objs = {}
        for prov_name, city_list in cities.items():
            province = province_objs[prov_name]
            for idx, city_name in enumerate(city_list, start=1):
                city, created = CityMunicipality.objects.get_or_create(
                    province=province,
                    name=city_name,
                    defaults={
                        "psgc_code": f"{province.psgc_code[:5]}{idx:02d}000",
                    },
                )
                city_objs[city_name] = city
                self.stdout.write(f"🏙 City: {city.name} ({'created' if created else 'exists'})")

        # --- Tourist Spots ---
        spots = [
            {"name": "Mayon Volcano", "description": "The iconic perfect cone volcano in Albay.", "city": "Legazpi City", "image": "locations/mayon.jpg"},
            {"name": "Cagsawa Ruins", "description": "Historic ruins with a backdrop of Mayon Volcano.", "city": "Daraga", "image": "locations/cagsawa.jpg"},
            {"name": "Bagasbas Beach", "description": "Popular surfing spot in Camarines Norte.", "city": "Daet", "image": "locations/bagasbas.jpg"},
            {"name": "Caramoan Islands", "description": "A paradise of hidden beaches and limestone cliffs.", "city": "Caramoan", "image": "locations/caramoan.jpg"},
            {"name": "CWC - Watersports Complex", "description": "World-class wakeboarding and watersports hub.", "city": "Naga City", "image": "locations/cwc.jpg"},
            {"name": "Binurong Point", "description": "Scenic cliffs and ocean views in Catanduanes.", "city": "Virac", "image": "locations/binurong.jpg"},
            {"name": "Ticao Island", "description": "Known for manta rays and rich marine biodiversity.", "city": "Masbate City", "image": "locations/ticao.jpg"},
            {"name": "Whale Shark Interaction", "description": "Swim with gentle giants in Donsol, Sorsogon.", "city": "Donsol", "image": "locations/whaleshark.jpg"},
            {"name": "Bulusan Lake", "description": "A serene eco-tourism spot surrounded by forest.", "city": "Sorsogon City", "image": "locations/bulusan.jpg"},
        ]

        for spot in spots:
            obj, created = TouristSpot.objects.get_or_create(
                slug=slugify(spot["name"]),
                city=city_objs[spot["city"]],
                defaults={
                    "name": spot["name"],
                    "description": spot["description"],
                    "image": spot["image"],
                    "is_featured": True,
                    "is_active": True,
                    "show_in_carousel": True,
                },
            )
            self.stdout.write(f"📍 Spot: {obj.name} ({'created' if created else 'exists'})")

        # --- Hotels ---
        hotels = [
            {"name": "The Oriental Legazpi", "city": "Legazpi City", "description": "Luxury hotel with Mayon Volcano views.", "image": "locations/hotel_oriental.jpg"},
            {"name": "Villa Caceres Hotel", "city": "Naga City", "description": "Blend of tradition and comfort.", "image": "locations/villa_caceres.jpg"},
            {"name": "Donsol Beachfront Inn", "city": "Donsol", "description": "Cozy inn near whale shark interaction sites.", "image": "locations/donsol_inn.jpg"},
        ]

        for hotel in hotels:
            obj, created = Hotel.objects.get_or_create(
                slug=slugify(hotel["name"]),
                city=city_objs[hotel["city"]],
                defaults={
                    "name": hotel["name"],
                    "description": hotel["description"],
                    "image": hotel["image"],
                    "is_active": True,
                },
            )
            self.stdout.write(f"🏨 Hotel: {obj.name} ({'created' if created else 'exists'})")

        # --- Restaurants ---
        restaurants = [
            {"name": "Small Talk Café", "city": "Legazpi City", "description": "Famous for Laing Pasta and Bicolano fusion.", "image": "locations/smalltalk.jpg"},
            {"name": "Bob Marlin", "city": "Naga City", "description": "Known for crispy pata and night gatherings.", "image": "locations/bobmarlin.jpg"},
            {"name": "Donsol Grill House", "city": "Donsol", "description": "Seafood and grilled dishes by the beach.", "image": "locations/donsol_grill.jpg"},
        ]

        for resto in restaurants:
            obj, created = Restaurant.objects.get_or_create(
                slug=slugify(resto["name"]),
                city=city_objs[resto["city"]],
                defaults={
                    "name": resto["name"],
                    "description": resto["description"],
                    "image": resto["image"],
                    "is_active": True,
                },
            )
            self.stdout.write(f"🍴 Restaurant: {obj.name} ({'created' if created else 'exists'})")

        self.stdout.write(self.style.SUCCESS("✅ Database seeding completed!"))
