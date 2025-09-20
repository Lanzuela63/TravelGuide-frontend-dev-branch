# apps/dashboards/urls/business_urls.py
from django.urls import path
from ..views import business_views as views

app_name = "dashboard_businesses"

urlpatterns = [
    path("", views.business_list, name="list"),
    path("add/", views.business_add, name="add"),
    path("<int:business_id>/edit/", views.business_edit, name="edit"),
    path("<int:business_id>/delete/", views.business_delete, name="delete"),
]