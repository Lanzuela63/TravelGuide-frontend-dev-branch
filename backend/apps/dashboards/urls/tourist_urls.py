# apps/dashboards/urls/tourist_urls.py
from django.urls import path
from ..views import tourist_views as views

app_name = "tourist_dash"

urlpatterns = [
    path("", views.tourist_dashboard, name="dashboard"),
    path("saved-spots/", views.tourist_saved_spots_list, name="saved_spots_list"),
]