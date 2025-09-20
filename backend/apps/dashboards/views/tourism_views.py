# apps/dashboards/views/tourism_views.py
from django.shortcuts import render
from apps.tourism.models import TouristSpot
from apps.dashboards.views.cards_utils import get_dashboard_cards


def tourism_dashboard(request):
    stats = {
        "total_spots": TouristSpot.objects.count(),
        "approved_spots": TouristSpot.objects.filter(is_active=True).count(),
        "pending_spots": TouristSpot.objects.filter(is_active=False).count(),
    }

    context = {
        "dashboard_cards": get_dashboard_cards("Tourism", stats),
        "latest_spots": TouristSpot.objects.filter(is_active=True).select_related("city")[:5],
    }
    return render(request, "dashboards/tourism_dashboard.html", context)




