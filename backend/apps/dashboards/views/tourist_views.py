# backend/apps/dashboards/views/tourist_views.py
from django.shortcuts import render, redirect, get_object_or_404
from apps.tourism.models import TouristSpot, SavedSpot
from apps.events.models import Event
from apps.ar.models import ARScene
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone # New import

User = get_user_model()

def is_tourist(user):
    return user.is_authenticated and user.role == 'Tourist'

@login_required
@user_passes_test(is_tourist)
def tourist_dashboard(request):
    # Recommended Tourist Spots (e.g., featured spots)
    recommended_spots = TouristSpot.objects.filter(is_featured=True)[:5]

    # Alerts for Events (upcoming events)
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:5]

    # Saved Destinations
    saved_spots = SavedSpot.objects.filter(user=request.user).select_related('spot')[:5]

    # Alerts for New AR Features (recently added AR scenes)
    new_ar_features = ARScene.objects.order_by('-created_at')[:5]

    context = {
        "welcome_message": f"Welcome, {request.user.first_name}!",
        "recommended_spots": recommended_spots,
        "upcoming_events": upcoming_events,
        "saved_spots": saved_spots,
        "new_ar_features": new_ar_features,
    }
    return render(request, "dashboards/tourist_dashboard.html", context)

@login_required
@user_passes_test(is_tourist)
def tourist_saved_spots_list(request):
    saved_spots = SavedSpot.objects.filter(user=request.user).select_related('spot')
    return render(request, "dashboards/tourist/tourist_saved_spots_list.html", {"saved_spots": saved_spots})