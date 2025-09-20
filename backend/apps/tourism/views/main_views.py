# apps/tourism/views/main_views.py
from django.shortcuts import render, get_object_or_404
from rest_framework import generics

from apps.tourism.models import (
    Province, Category, TouristSpot,
    Hotel, Restaurant, Review,
    Gallery, OperatingHour
)
from apps.tourism.serializers import (
    ProvinceSerializer, CategorySerializer, TouristSpotSerializer, TouristSpotDetailSerializer,
    HotelSerializer, RestaurantSerializer,
    ReviewSerializer, GallerySerializer,
    OperatingHourSerializer
)


# -------------------------
# Province Views
# -------------------------
class ProvinceListCreateView(generics.ListCreateAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer


class ProvinceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer


# -------------------------
# Category Views
# -------------------------
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# -------------------------
# Tourist Spot Views
# -------------------------
class TouristSpotListCreateView(generics.ListCreateAPIView):
    queryset = TouristSpot.objects.all()
    serializer_class = TouristSpotSerializer


class TouristSpotDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TouristSpot.objects.all()
    serializer_class = TouristSpotSerializer


class TouristSpotFullDetailView(generics.RetrieveAPIView):
    queryset = TouristSpot.objects.all()
    serializer_class = TouristSpotDetailSerializer


# -------------------------
# Hotel Views
# -------------------------
class HotelListCreateView(generics.ListCreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


class HotelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


# -------------------------
# Restaurant Views
# -------------------------
class RestaurantListCreateView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


# -------------------------
# Review Views
# -------------------------
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


# -------------------------
# Gallery Views
# -------------------------
class GalleryListCreateView(generics.ListCreateAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer


class GalleryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer


# -------------------------
# Operating Hour Views
# -------------------------
class OperatingHourListCreateView(generics.ListCreateAPIView):
    queryset = OperatingHour.objects.all()
    serializer_class = OperatingHourSerializer


class OperatingHourDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OperatingHour.objects.all()
    serializer_class = OperatingHourSerializer


# -------------------------
# Public Pages (HTML)
# -------------------------
def public_home(request):
    return render(request, "tourism/index.html")

def about(request):
    return render(request, "tourism/about.html")

def gallery(request):
    return render(request, "tourism/gallery.html")

def contact(request):
    return render(request, "tourism/contact.html")

def hotels(request):
    return render(request, "tourism/hotels.html")

def blogd(request):
    return render(request, "tourism/blog.html")

def explore_spots(request):
    return render(request, "tourism/explore_spots.html")

def places_to_go(request):
    return render(request, "tourism/places_to_go.html")

def plan_your_trip(request):
    return render(request, "tourism/plan_your_trip.html")

def saved_spots(request):
    return render(request, "tourism/saved_spots.html")

def review_spots(request):
    return render(request, "tourism/review_spots.html")

def spot_detail_view(request, pk):
    return render(request, "tourism/spot_detail.html", {"pk": pk})


def province_spots(request, province_slug):
    """Render all tourist spots, hotels, and restaurants for a given province.
    Works with HTMX (modal) or as a normal view."""
    
    province = get_object_or_404(Province, slug=province_slug)
    spots = TouristSpot.objects.filter(city__province=province, is_active=True)
    hotels = Hotel.objects.filter(city__province=province, is_active=True)
    restaurants = Restaurant.objects.filter(city__province=province, is_active=True)

    return render(request, "tourism/partials/province_spot_cards.html", {
        "province": province,
        "spots": spots,
        "hotels": hotels,
        "restaurants": restaurants,
    })