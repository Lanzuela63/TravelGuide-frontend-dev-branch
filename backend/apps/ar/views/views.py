#apps/ar/views/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def webar_view(request, spot_id=None):
    context = {'spot_id': spot_id}
    return render(request, 'ar/webar_scene.html', context)

def location_ar_view(request):
    # For now, just pass some dummy data
    context = {
        'message': 'Location AR View - Backend is working!',
        'latitude': 0.0,
        'longitude': 0.0,
    }
    return render(request, 'ar/location_ar_scene.html', context)

@login_required
def ar_experience_view(request):
    """
    Renders the AR experience page.
    Only logged-in users can access.
    """
    return render(request, "ar/ar_experience.html")
