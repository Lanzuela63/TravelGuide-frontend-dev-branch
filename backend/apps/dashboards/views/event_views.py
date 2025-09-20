# apps/dashboards/views/event_views.py
from django.shortcuts import render
from apps.events.models import Event
from apps.dashboards.views.cards_utils import get_dashboard_cards


def event_dashboard(request):
    stats = {
        "total_events": Event.objects.count(),
        "upcoming_events": Event.objects.filter(status="upcoming").count(),
        "past_events": Event.objects.filter(status="past").count(),
    }

    context = {
        "dashboard_cards": get_dashboard_cards("Event", stats),
        "latest_events": Event.objects.order_by("-created_at")[:5],
    }
    return render(request, "dashboards/event_dashboard.html", context)


