# apps/ar/urls.py
from django.urls import path
from .views import views

app_name = "ar"

urlpatterns = [
    path("webar/<int:spot_id>/", views.webar_view, name="webar_view"),
    path("location/", views.location_ar_view, name="location_ar_view"),
    path("experience/", views.ar_experience_view, name="ar_experience"),
]

