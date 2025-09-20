import django_filters
from .models import TouristSpot

class TouristSpotFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    location = django_filters.CharFilter(field_name='location__name', lookup_expr='icontains')

    class Meta:
        model = TouristSpot
        fields = ['name', 'category', 'location']
