# apps/tourism/urls/api_urls.py (API endpoints)
# apps/tourism/urls/api_urls.py
from django.urls import path
from apps.tourism.views import api_views as api

app_name = "tourism_api"

urlpatterns = [
    # Location cascading dropdowns
    path("get_cities/", api.get_cities, name="get_cities"),
    path("get_barangays/", api.get_barangays, name="get_barangays"),

    # Provinces & Cities
    path("provinces/", api.ProvinceListAPIView.as_view(), name="api-provinces"),
    path("cities/", api.CityMunicipalityListAPIView.as_view(), name="api-cities"),
    path("cities/", api.CityMunicipalityListAPIView.as_view(), name="city-list"),

    # Categories
    path("categories/", api.CategoryListAPIView.as_view(), name="api-categories"),

    # Tourist Spots
    path("spots/", api.TouristSpotListAPIView.as_view(), name="api-spots"),
    path("spots/<int:pk>/", api.TouristSpotDetailAPIView.as_view(), name="api-spot-detail"),

    # Hotels & Restaurants
    path("hotels/", api.HotelListAPIView.as_view(), name="api-hotels"),
    path("restaurants/", api.RestaurantListAPIView.as_view(), name="api-restaurants"),

    # Reviews
    path("reviews/", api.ReviewListAPIView.as_view(), name="api-reviews"),
    path("reviews/create/", api.ReviewCreateAPIView.as_view(), name="api-review-create"),

    # Gallery & Hours
    path("gallery/", api.GalleryListAPIView.as_view(), name="api-gallery"),
    path("hours/", api.OperatingHourListAPIView.as_view(), name="api-hours"),

    # Saved & Visited
    path("saved/", api.SavedSpotListCreateAPIView.as_view(), name="api-saved"),
    path("visited/", api.VisitedSpotListCreateAPIView.as_view(), name="api-visited"),
]
