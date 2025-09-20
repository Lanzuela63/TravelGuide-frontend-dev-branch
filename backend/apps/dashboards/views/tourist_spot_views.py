# backend/apps/dashboards/views/tourist_spot_views.py
from django.shortcuts import render, redirect, get_object_or_404
from apps.tourism.models import TouristSpot
from ..forms import TouristSpotForm


def spot_list(request):
    spots = TouristSpot.objects.all()
    return render(request, "dashboards/tourist_spots/spot_list.html", {"spots": spots})

def spot_add(request):
    if request.method == "POST":
        form = TouristSpotForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("admin_dash:spots:list")
    else:
        form = TouristSpotForm()
    return render(request, "dashboards/tourist_spots/spot_form.html", {"form": form})

def spot_edit(request, spot_id):
    spot = get_object_or_404(TouristSpot, id=spot_id)
    if request.method == "POST":
        form = TouristSpotForm(request.POST, request.FILES, instance=spot)
        if form.is_valid():
            form.save()
            return redirect("admin_dash:spots:list")
    else:
        form = TouristSpotForm(instance=spot)
    return render(request, "dashboards/tourist_spots/spot_form.html", {"form": form, "spot": spot})

def spot_delete(request, spot_id):
    spot = get_object_or_404(TouristSpot, id=spot_id)
    if request.method == "POST":
        spot.delete()
        return redirect("admin_dash:spots:list")
    return render(request, "dashboards/tourist_spots/spot_confirm_delete.html", {"spot": spot})