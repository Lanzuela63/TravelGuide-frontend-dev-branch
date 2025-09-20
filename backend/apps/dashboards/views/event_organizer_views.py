# backend/apps/dashboards/views/event_organizer_views.py
from django.shortcuts import render, redirect, get_object_or_404
from apps.events.models import Event
from ..forms import EventForm
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.contrib.auth.decorators import login_required, user_passes_test # New import
from django.contrib.auth import get_user_model # New import

User = get_user_model() # Get CustomUser model

def is_event_organizer(user):
    return user.is_authenticated and user.role == 'Event Organizer'

@login_required
@user_passes_test(is_event_organizer)
def event_organizer_dashboard(request):
    user_events = Event.objects.filter(organizer=request.user)

    my_events_count = user_events.count()
    pending_events_count = user_events.filter(is_approved=False).count()
    total_approved_events = my_events_count - pending_events_count

    # Data for Approval Status Pie Chart
    approved_count = user_events.filter(is_approved=True).count()
    pending_count = user_events.filter(is_approved=False).count()
    
    approval_chart_data = {
        "labels": ["Approved", "Pending"],
        "data": [approved_count, pending_count],
    }

    # Data for Event Creation Trend Line Chart
    creation_trend = user_events.annotate(month=TruncMonth('created_at')) \
                                    .values('month') \
                                    .annotate(count=Count('id')) \
                                    .order_by('month')
    
    creation_chart_labels = [month['month'].strftime('%Y-%m') for month in creation_trend]
    creation_chart_data = [month['count'] for month in creation_trend]

    context = {
        "welcome_message": f"Welcome, {request.user.first_name}!",
        "my_events_count": my_events_count,
        "pending_events_count": pending_events_count,
        "total_approved_events": total_approved_events,
        "latest_events": user_events.order_by('-created_at')[:5], # Latest 5 events
        "approval_chart_data": approval_chart_data,
        "creation_chart_labels": creation_chart_labels,
        "creation_chart_data": creation_chart_data,
    }
    return render(request, "dashboards/event_organizer_dashboard.html", context)

@login_required
@user_passes_test(is_event_organizer)
def event_organizer_event_list(request):
    events = Event.objects.filter(organizer=request.user)
    return render(request, "dashboards/events/event_organizer_event_list.html", {"events": events})

@login_required
@user_passes_test(is_event_organizer)
def event_organizer_event_add(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user # Assign current user as organizer
            event.save()
            return redirect("event_organizer_dash:event_list")
    else:
        form = EventForm(initial={'organizer': request.user})
    return render(request, "dashboards/events/event_organizer_event_form.html", {"form": form})

@login_required
@user_passes_test(is_event_organizer)
def event_organizer_event_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id, organizer=request.user)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("event_organizer_dash:event_list")
    else:
        form = EventForm(instance=event)
    return render(request, "dashboards/events/event_organizer_event_form.html", {"form": form, "event": event})

@login_required
@user_passes_test(is_event_organizer)
def event_organizer_event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id, organizer=request.user)
    if request.method == "POST":
        event.delete()
        return redirect("event_organizer_dash:event_list")
    return render(request, "dashboards/events/event_organizer_event_confirm_delete.html", {"event": event})