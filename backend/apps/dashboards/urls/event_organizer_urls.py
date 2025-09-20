# apps/dashboards/urls/event_organizer_urls.py
from django.urls import path
from ..views import event_organizer_views as views

app_name = "event_organizer_dash"

urlpatterns = [
    path("", views.event_organizer_dashboard, name="dashboard"),
    path("my-events/", views.event_organizer_event_list, name="event_list"),
    path("my-events/add/", views.event_organizer_event_add, name="event_add"),
    path("my-events/<int:event_id>/edit/", views.event_organizer_event_edit, name="event_edit"),
    path("my-events/<int:event_id>/delete/", views.event_organizer_event_delete, name="event_delete"),
]
