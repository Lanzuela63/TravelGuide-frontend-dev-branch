# backend/urls.py (project-level)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apps.tourism.views.api_views import TouristSpotListAPIView

urlpatterns = [
    path("admin/", admin.site.urls),

    # Authentication & user system
    path("", include("apps.users.urls")),
    path("accounts/", include("apps.users.urls")),
    path("accounts/", include("allauth.urls")),

    # Public modules
    path("tourism/", include(("apps.tourism.urls.urls", "tourism"), namespace="tourism")),
    path("business/", include(("apps.business.urls", "businesses"), namespace="businesses")),
    path("events/", include(("apps.events.urls", "events"), namespace="events")),
    path("ar/", include("apps.ar.urls", namespace="ar")),  # AR page views

    # API routes
    # path("api/tourism-spots/", TouristSpotListAPIView.as_as_view(), name="tourism-spot-list"),
    path("api/tourism/", include("apps.tourism.urls.api_urls", namespace="tourism_api")),
    path("api/ar/", include("apps.ar.api_urls", namespace="ar_api")),

    # Dashboards
    path("dashboard/admin/", include(("apps.dashboards.urls.admin_urls", "admin_dash"), namespace="admin_dash")),
    path("dashboard/tourism/", include(("apps.dashboards.urls.tourism_urls", "tourism_dash"), namespace="tourism_dash")),
    path("dashboard/business/", include(("apps.dashboards.urls.business_urls", "business_dash"), namespace="business_dash")),
    path("dashboard/event/", include(("apps.dashboards.urls.event_urls", "event_dash"), namespace="event_dash")),
    path("dashboard/tourist/", include(("apps.dashboards.urls.tourist_urls", "tourist_dash"), namespace="tourist_dash")),
    path("dashboard/business-owner/", include(("apps.dashboards.urls.business_owner_urls", "business_owner_dash"), namespace="business_owner_dash")),
    path("dashboard/event-organizer/", include(("apps.dashboards.urls.event_organizer_urls", "event_organizer_dash"), namespace="event_organizer_dash")),
    path("dashboard/tourism-officer/", include(("apps.dashboards.urls.tourism_officer_urls", "tourism_officer_dash"), namespace="tourism_officer_dash")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
