# apps/tourism/views/api_views.py
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

from apps.tourism.models import (
    Province, CityMunicipality, Barangay, Category, TouristSpot,
    Hotel, Restaurant, Review, Gallery, OperatingHour,
    SavedSpot, VisitedSpot
)
from apps.tourism.serializers import (
    ProvinceSerializer, CityMunicipalitySerializer, CategorySerializer,
    TouristSpotSerializer, TouristSpotDetailSerializer,
    HotelSerializer, RestaurantSerializer,
    ReviewSerializer, GallerySerializer, OperatingHourSerializer,
    SavedSpotSerializer, VisitedSpotSerializer
)


# -------------------------
# Location Endpoints
# -------------------------
def get_cities(request):
    province_id = request.GET.get('parent_id')
    cities = CityMunicipality.objects.filter(province_id=province_id).order_by('name')
    return JsonResponse(list(cities.values('id', 'name')), safe=False)

def get_barangays(request):
    city_id = request.GET.get('parent_id')
    barangays = Barangay.objects.filter(city_id=city_id).order_by('name')
    return JsonResponse(list(barangays.values('id', 'name')), safe=False)

# -------------------------
# Province & City Endpoints
# -------------------------
class ProvinceListAPIView(generics.ListAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    permission_classes = [AllowAny]
    

class ProvinceCitiesAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        """Return all cities belonging to a given province"""
        try:
            province = Province.objects.get(pk=pk)
        except Province.DoesNotExist:
            return Response({"error": "Province not found"}, status=404)

        cities = CityMunicipality.objects.filter(province=province)
        serializer = CityMunicipalitySerializer(cities, many=True)
        return Response(serializer.data)    


class CityMunicipalityListAPIView(generics.ListAPIView):
    queryset = CityMunicipality.objects.select_related("province").all()
    serializer_class = CityMunicipalitySerializer
    permission_classes = [AllowAny]


# -------------------------
# Category Endpoints
# -------------------------
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


# -------------------------
# Tourist Spots
# -------------------------
class TouristSpotListAPIView(generics.ListAPIView):
    queryset = TouristSpot.objects.select_related("city__province").all()
    serializer_class = TouristSpotSerializer
    permission_classes = [AllowAny]


class TouristSpotDetailAPIView(generics.RetrieveAPIView):
    queryset = TouristSpot.objects.select_related("city__province").all()
    serializer_class = TouristSpotDetailSerializer
    permission_classes = [AllowAny]


# -------------------------
# Hotels & Restaurants
# -------------------------
class HotelListAPIView(generics.ListAPIView):
    queryset = Hotel.objects.select_related("city__province").all()
    serializer_class = HotelSerializer
    permission_classes = [AllowAny]


class RestaurantListAPIView(generics.ListAPIView):
    queryset = Restaurant.objects.select_related("city__province").all()
    serializer_class = RestaurantSerializer
    permission_classes = [AllowAny]


# -------------------------
# Reviews
# -------------------------
class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewListAPIView(generics.ListAPIView):
    queryset = Review.objects.select_related("user").all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]


# -------------------------
# Gallery & Operating Hours
# -------------------------
class GalleryListAPIView(generics.ListAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = [AllowAny]


class OperatingHourListAPIView(generics.ListAPIView):
    queryset = OperatingHour.objects.all()
    serializer_class = OperatingHourSerializer
    permission_classes = [AllowAny]


# -------------------------
# Saved & Visited Spots
# -------------------------
class SavedSpotListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = SavedSpotSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SavedSpot.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VisitedSpotListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = VisitedSpotSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return VisitedSpot.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
