# apps/dashboards/urls/user_urls.py
from django.urls import path
from ..views import user_views as views

app_name = "dashboard_users"

urlpatterns = [
    path("", views.user_list, name="list"),
    path("add/", views.user_add, name="add"),
    path("<int:user_id>/edit/", views.user_edit, name="edit"),
    path("<int:user_id>/delete/", views.user_delete, name="delete"),
]
