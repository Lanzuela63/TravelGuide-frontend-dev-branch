# apps/tourism/serializers.py
from rest_framework import serializers
from .models import (
    Province, CityMunicipality, Category, TouristSpot,
    Hotel, Restaurant, Review, Gallery, OperatingHour,
    SavedSpot, VisitedSpot
)


# -------------------------------
# Province & City
# -------------------------------
class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = "__all__"


class CityMunicipalitySerializer(serializers.ModelSerializer):
    province = ProvinceSerializer(read_only=True)

    class Meta:
        model = CityMunicipality
        fields = "__all__"


# -------------------------------
# Category
# -------------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


# -------------------------------
# Base Location Serializers
# -------------------------------
class TouristSpotSerializer(serializers.ModelSerializer):
    province = ProvinceSerializer(source="city.province", read_only=True)
    city = CityMunicipalitySerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = TouristSpot
        fields = [
            "id", "name", "description", "image",
            "province", "city", "categories",
            "is_featured", "show_in_carousel", "average_rating"
        ]


class HotelSerializer(serializers.ModelSerializer):
    province = ProvinceSerializer(source="city.province", read_only=True)
    city = CityMunicipalitySerializer(read_only=True)

    class Meta:
        model = Hotel
        fields = "__all__"


class RestaurantSerializer(serializers.ModelSerializer):
    province = ProvinceSerializer(source="city.province", read_only=True)
    city = CityMunicipalitySerializer(read_only=True)

    class Meta:
        model = Restaurant
        fields = "__all__"


# -------------------------------
# Review
# -------------------------------
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    location = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"


# -------------------------------
# Gallery & Operating Hours
# -------------------------------
class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = "__all__"


class OperatingHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperatingHour
        fields = "__all__"


# -------------------------------
# Detailed Location Serializer
# -------------------------------
class TouristSpotDetailSerializer(serializers.ModelSerializer):
    province = ProvinceSerializer(source="city.province", read_only=True)
    city = CityMunicipalitySerializer(read_only=True)
    categories = CategorySerializer(many=True, source="categories", read_only=True)
    reviews = ReviewSerializer(many=True, source="review_set", read_only=True)
    gallery = GallerySerializer(many=True, source="gallery_set", read_only=True)
    operating_hours = OperatingHourSerializer(many=True, source="operatinghour_set", read_only=True)

    class Meta:
        model = TouristSpot
        fields = "__all__"


# -------------------------------
# Saved / Visited Spots
# -------------------------------
class SavedSpotSerializer(serializers.ModelSerializer):
    spot = TouristSpotSerializer(read_only=True)

    class Meta:
        model = SavedSpot
        fields = "__all__"


class VisitedSpotSerializer(serializers.ModelSerializer):
    spot = TouristSpotSerializer(read_only=True)

    class Meta:
        model = VisitedSpot
        fields = "__all__"
