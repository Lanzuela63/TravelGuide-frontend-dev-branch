# apps/dashboards/urls/tourist_spot_urls.py
from django.urls import path
from ..views import tourist_spot_views as views

app_name = "dashboard_spots"

urlpatterns = [
    path("", views.spot_list, name="list"),
    path("add/", views.spot_add, name="add"),
    path("<int:spot_id>/edit/", views.spot_edit, name="edit"),
    path("<int:spot_id>/delete/", views.spot_delete, name="delete"),
]
