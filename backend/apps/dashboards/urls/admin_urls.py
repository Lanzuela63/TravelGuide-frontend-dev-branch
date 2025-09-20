# apps/dashboards/urls/admin_urls.py
from django.urls import path, include
from apps.dashboards.views import admin_views
from apps.dashboards.views import psgc_views
from apps.dashboards.views import business_views

app_name = "admin_dash"

urlpatterns = [
    path('', admin_views.admin_dashboard, name="dashboard"),
    path("add-city/", psgc_views.add_city, name="add_city"),
    path('get-cities/', psgc_views.get_cities, name='get_cities'),
    path('get-barangays/', psgc_views.get_barangays, name='get_barangays'),
    path("chart-data/", admin_views.chart_data, name="chart_data"),
    path("spots/", include(("apps.dashboards.urls.tourist_spot_urls", "spots"), namespace="spots")),
    path("users/", include(("apps.dashboards.urls.user_urls", "users"), namespace="users")),
    path("ar-scenes/", include(("apps.dashboards.urls.ar_scene_urls", "ar_scenes"), namespace="ar_scenes")),
    path("businesses/", include(("apps.dashboards.urls.business_urls", "businesses"), namespace="businesses")),
    path("pending-businesses/", business_views.admin_pending_businesses_list, name="pending_businesses_list"),
    path("approve-business/<int:business_id>/", business_views.approve_business, name="approve_business"),
    path("pending-events/", admin_views.admin_pending_events_list, name="pending_events_list"), # New URL
]