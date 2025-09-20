# apps/tourism/management/commands/update_psgc.py
import requests
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.tourism.models import Region, Province, CityMunicipality, Barangay

PSGC_API = "https://psgc.cloud/api/v2"
BICOL_REGION_CODE = "0500000000"

class Command(BaseCommand):
    help = "Sync PSGC Provinces, Cities/Municipalities, and Barangays for Region V (Bicol)"

    def handle(self, *args, **kwargs):
        self.stdout.write("🔄 Syncing PSGC data for Region V…")

        # Regions
        regions = requests.get(f"{PSGC_API}/regions").json()["data"]
        bicol_region_data = [r for r in regions if r["code"] == BICOL_REGION_CODE][0]
        region, _ = Region.objects.update_or_create(
            psgc_code=bicol_region_data["code"],
            defaults={"name": bicol_region_data["name"]}
        )

        # Provinces under Region V
        provinces = requests.get(f"{PSGC_API}/regions/{bicol_region_data['code']}/provinces").json()["data"]

        for p in provinces:
            province, _ = Province.objects.update_or_create(
                psgc_code=p["code"],
                defaults={"name": p["name"], "slug": slugify(p["name"]), "region": region}
            )

        # Cities & Municipalities under those provinces
        for p in provinces:
            cities = requests.get(f"{PSGC_API}/provinces/{p['code']}/cities-municipalities").json()["data"]
            for c in cities:
                province = Province.objects.get(psgc_code=p["code"])
                CityMunicipality.objects.update_or_create(
                    psgc_code=c["code"],
                    defaults={"name": c["name"], "province": province}
                )

        # Barangays under those cities
        for p in provinces:
            cities = requests.get(f"{PSGC_API}/provinces/{p['code']}/cities-municipalities").json()["data"]
            for c in cities:
                barangays = requests.get(f"{PSGC_API}/cities-municipalities/{c['code']}/barangays").json()["data"]
                city = CityMunicipality.objects.get(psgc_code=c["code"])
                for b in barangays:
                    Barangay.objects.update_or_create(
                        psgc_code=b["code"],
                        defaults={"name": b["name"], "city": city}
                    )

        self.stdout.write(self.style.SUCCESS("✅ PSGC data sync for Region V completed!"))