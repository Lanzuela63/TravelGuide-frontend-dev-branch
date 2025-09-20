from django.shortcuts import render
from django.http import JsonResponse
from django.db.models.functions import TruncDate
from django.db.models import Count
from django.db import models
from django.contrib.auth import get_user_model
from apps.tourism.models import TouristSpot, Review
from apps.events.models import Event # Import Event model
from apps.business.models import Business
from apps.tourism.models import Province, VisitedSpot
from apps.ar.models import ARScene
from django.contrib.auth.decorators import login_required, user_passes_test

User = get_user_model()

def is_admin(user):
    return user.is_authenticated and user.role == 'Admin' # Using CustomUser role

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Data for cards
    spots_count = TouristSpot.objects.count()
    users_count = User.objects.count()
    ar_count = ARScene.objects.count()
    
    # Calculate total pending requests (businesses + events)
    pending_businesses_count = Business.objects.filter(is_approved=False).count()
    pending_events_count = Event.objects.filter(is_approved=False).count()
    pending_requests = pending_businesses_count + pending_events_count

    context = {
        "spots_count": spots_count,
        "users_count": users_count,
        "ar_count": ar_count,
        "pending_requests": pending_requests,
        "latest_spots": TouristSpot.objects.filter(is_active=True).select_related("city")[:5],
        "provinces": Province.objects.all(),    
    }
    
    return render(request, "dashboards/admin_dashboard.html", context)

@login_required
@user_passes_test(is_admin) # Chart data should also be restricted
def chart_data(request):
    users_count = User.objects.count()
    spots_count = TouristSpot.objects.count()

    visits = (
        VisitedSpot.objects
        .annotate(day=TruncDate('visited_at'))
        .values('day')
        .annotate(total=Count('id'))
        .order_by('day')
    )

    labels = [str(v['day']) for v in visits]
    data = [v['total'] for v in visits]

    return JsonResponse({
        "labels": labels,
        "data": data,
        "users": users_count,
        "spots": spots_count,
    })

@login_required
@user_passes_test(is_admin)
def admin_pending_events_list(request):
    pending_events = Event.objects.filter(is_approved=False)
    return render(request, "dashboards/events/admin_pending_events_list.html", {"events": pending_events})