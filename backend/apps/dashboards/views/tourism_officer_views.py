# backend/apps/dashboards/views/tourism_officer_views.py
from django.shortcuts import render, redirect, get_object_or_404
from apps.tourism.models import TouristSpot
from ..forms import TouristSpotForm
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from apps.events.models import Event

User = get_user_model()

def is_tourism_officer(user):
    return user.is_authenticated and user.role == 'Tourism Officer'

@login_required
@user_passes_test(is_tourism_officer)
def tourism_officer_dashboard(request):
    # Dashboard data for Tourism Officer
    total_spots_count = TouristSpot.objects.count()
    active_spots_count = TouristSpot.objects.filter(is_active=True).count()
    inactive_spots_count = TouristSpot.objects.filter(is_active=False).count()

    # Data for Spot Status Pie Chart
    spot_status_chart_data = {
        "labels": ["Active", "Inactive"],
        "data": [active_spots_count, inactive_spots_count],
    }

    # Data for Spot Creation Trend Line Chart
    creation_trend = TouristSpot.objects.annotate(month=TruncMonth('created_at')) \
                                    .values('month') \
                                    .annotate(count=Count('id')) \
                                    .order_by('month')
    
    creation_chart_labels = [month['month'].strftime('%Y-%m') for month in creation_trend]
    creation_chart_data = [month['count'] for month in creation_trend]

    # Event Calendar Data
    events = Event.objects.all() # Fetch all events
    calendar_events = []
    for event in events:
        calendar_events.append({
            'title': event.title,
            'start': event.date.isoformat(),
            'end': event.date.isoformat(),
            'description': event.description,
            'location': event.location,
            'time': event.time.strftime('%H:%M'),
        })

    context = {
        "welcome_message": f"Welcome, {request.user.first_name}!",
        "total_spots_count": total_spots_count,
        "active_spots_count": active_spots_count,
        "inactive_spots_count": inactive_spots_count,
        "spot_status_chart_data": spot_status_chart_data,
        "creation_chart_labels": creation_chart_labels,
        "creation_chart_data": creation_chart_data,
        "latest_spots": TouristSpot.objects.order_by('-created_at')[:5],
        "calendar_events": calendar_events,
    }
    return render(request, "dashboards/tourism_officer_dashboard.html", context)

@login_required
@user_passes_test(is_tourism_officer)
def tourism_officer_spot_list(request):
    spots = TouristSpot.objects.all()
    return render(request, "dashboards/tourism_officer/tourism_officer_spot_list.html", {"spots": spots})

@login_required
@user_passes_test(is_tourism_officer)
def tourism_officer_spot_add(request):
    if request.method == "POST":
        form = TouristSpotForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("tourism_officer_dash:spot_list")
    else:
        form = TouristSpotForm()
    return render(request, "dashboards/tourism_officer/tourism_officer_spot_form.html", {"form": form})

@login_required
@user_passes_test(is_tourism_officer)
def tourism_officer_spot_edit(request, spot_id):
    spot = get_object_or_404(TouristSpot, id=spot_id)
    if request.method == "POST":
        form = TouristSpotForm(request.POST, request.FILES, instance=spot)
        if form.is_valid():
            form.save()
            return redirect("tourism_officer_dash:spot_list")
    else:
        form = TouristSpotForm(instance=spot)
    return render(request, "dashboards/tourism_officer/tourism_officer_spot_form.html", {"form": form, "spot": spot})

@login_required
@user_passes_test(is_tourism_officer)
def tourism_officer_spot_delete(request, spot_id):
    spot = get_object_or_404(TouristSpot, id=spot_id)
    if request.method == "POST":
        spot.delete()
        return redirect("tourism_officer_dash:spot_list")
    return render(request, "dashboards/tourism_officer/tourism_officer_spot_confirm_delete.html", {"spot": spot})

@login_required
@user_passes_test(is_tourism_officer)
def tourism_officer_pending_events_list(request):
    pending_events = Event.objects.filter(is_approved=False)
    return render(request, "dashboards/events/tourism_officer_pending_events_list.html", {"events": pending_events})

@login_required
@user_passes_test(is_tourism_officer)
def approve_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        event.is_approved = True
        event.save()
        # Optionally add a success message
        return redirect("tourism_officer_dash:pending_events_list")
    return redirect("tourism_officer_dash:pending_events_list") # Redirect if not POST
