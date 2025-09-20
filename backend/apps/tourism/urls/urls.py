# apps/tourism/urls/urls.py
from django.urls import path
from apps.tourism.views import main_views as views

app_name = "tourism"

urlpatterns = [
    # Provinces
    path("provinces/", views.ProvinceListCreateView.as_view(), name="province-list"),
    path("provinces/<int:pk>/", views.ProvinceDetailView.as_view(), name="province-detail"),

    # Categories
    path("categories/", views.CategoryListCreateView.as_view(), name="category-list"),
    path("categories/<int:pk>/", views.CategoryDetailView.as_view(), name="category-detail"),

    # Tourist Spots
    path("spots/", views.TouristSpotListCreateView.as_view(), name="spot-list"),
    path("spots/<int:pk>/", views.TouristSpotDetailView.as_view(), name="spot-detail"),
    path("spots/<int:pk>/full/", views.TouristSpotFullDetailView.as_view(), name="spot-full-detail"),

    # Hotels & Restaurants
    path("hotels/", views.HotelListCreateView.as_view(), name="hotel-list"),
    path("hotels/<int:pk>/", views.HotelDetailView.as_view(), name="hotel-detail"),
    path("restaurants/", views.RestaurantListCreateView.as_view(), name="restaurant-list"),
    path("restaurants/<int:pk>/", views.RestaurantDetailView.as_view(), name="restaurant-detail"),

    # Reviews
    path("reviews/", views.ReviewListCreateView.as_view(), name="review-list"),
    path("reviews/<int:pk>/", views.ReviewDetailView.as_view(), name="review-detail"),

    # Gallery
    path("gallery/", views.GalleryListCreateView.as_view(), name="gallery-list"),
    path("gallery/<int:pk>/", views.GalleryDetailView.as_view(), name="gallery-detail"),

    # Operating Hours
    path("hours/", views.OperatingHourListCreateView.as_view(), name="hour-list"),
    path("hours/<int:pk>/", views.OperatingHourDetailView.as_view(), name="hour-detail"),

    # Public HTML Pages
    path("", views.public_home, name="index"),
    path("about/", views.about, name="about"),
    path("gallery/", views.gallery, name="gallery"),
    path("contact/", views.contact, name="contact"),
    path("hotels/", views.contact, name="hotels"),
    path("blog/", views.blogd, name="blog"),
    
    path("explore/", views.explore_spots, name="explore_spots"),
    path("places/", views.places_to_go, name="places_to_go"),
    path("plan/", views.plan_your_trip, name="plan_your_trip"),
    path("saved/", views.saved_spots, name="saved_spots"),
    path("spots/<int:pk>/detail/", views.spot_detail_view, name="spot_detail_page"),
    path("province/<slug:province_slug>/", views.province_spots, name="province_spots"),
]
