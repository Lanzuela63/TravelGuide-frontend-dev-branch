from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from apps.tourism.models import Province, CityMunicipality, Barangay


def get_psgc_context():
    return {
        "provinces": Province.objects.all(),
        "cities": CityMunicipality.objects.select_related("province").all()
    }


@require_POST
def add_city(request):
    province_id = request.POST.get("province")
    city_name = request.POST.get("city")
    if province_id and city_name:
        CityMunicipality.objects.create(province_id=province_id, name=city_name)
    cities = CityMunicipality.objects.select_related("province").all()
    return render(request, "dashboards/partials/_city_list.html", {"cities": cities})


def get_cities(request):
    province_id = request.GET.get('province_id')
    cities = CityMunicipality.objects.filter(province_id=province_id).values('id', 'name')
    return JsonResponse(list(cities), safe=False)


def get_barangays(request):
    city_id = request.GET.get('city_id')
    barangays = Barangay.objects.filter(city_id=city_id).values('id', 'name')
    return JsonResponse(list(barangays), safe=False)

