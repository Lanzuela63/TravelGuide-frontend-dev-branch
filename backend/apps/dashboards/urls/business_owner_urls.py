# apps/dashboards/urls/business_owner_urls.py
from django.urls import path
from ..views import business_owner_views as views

app_name = "business_owner_dash"

urlpatterns = [
    path("", views.business_owner_dashboard, name="dashboard"),
    path("my-businesses/", views.business_owner_business_list, name="business_list"),
    path("my-businesses/add/", views.business_owner_business_add, name="business_add"),
    path("my-businesses/<int:business_id>/edit/", views.business_owner_business_edit, name="business_edit"),
    path("my-businesses/<int:business_id>/delete/", views.business_owner_business_delete, name="business_delete"),
]