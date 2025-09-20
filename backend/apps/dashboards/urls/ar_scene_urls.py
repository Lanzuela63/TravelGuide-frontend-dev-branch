# apps/dashboards/urls/ar_scene_urls.py
from django.urls import path
from ..views import ar_scene_views as views

app_name = "dashboard_ar_scenes"

urlpatterns = [
    path("", views.ar_scene_list, name="list"),
    path("add/", views.ar_scene_add, name="add"),
    path("<int:scene_id>/edit/", views.ar_scene_edit, name="edit"),
    path("<int:scene_id>/delete/", views.ar_scene_delete, name="delete"),
]
