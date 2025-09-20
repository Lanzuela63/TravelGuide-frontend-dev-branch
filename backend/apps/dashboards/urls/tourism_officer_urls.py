# apps/dashboards/urls/tourism_officer_urls.py
from django.urls import path
from ..views import tourism_officer_views as views

app_name = "tourism_officer_dash"

urlpatterns = [
    path("", views.tourism_officer_dashboard, name="dashboard"),
    path("tourist-spots/", views.tourism_officer_spot_list, name="spot_list"),
    path("tourist-spots/add/", views.tourism_officer_spot_add, name="spot_add"),
    path("tourist-spots/<int:spot_id>/edit/", views.tourism_officer_spot_edit, name="spot_edit"),
    path("tourist-spots/<int:spot_id>/delete/", views.tourism_officer_spot_delete, name="spot_delete"),
    path("pending-events/", views.tourism_officer_pending_events_list, name="pending_events_list"),
    path("approve-event/<int:event_id>/", views.approve_event, name="approve_event"), # New URL
]
