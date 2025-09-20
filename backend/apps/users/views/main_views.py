from django.shortcuts import render, redirect
from django.urls import reverse

def public_home(request):
    return render(request, 'tourism/index.html')

def dashboard_redirect_view(request):
    if not request.user.is_authenticated:
        return redirect('account_login') # Redirect to login if not authenticated

    role = request.user.role

    if role == 'Admin':
        return redirect(reverse('admin_dash:dashboard'))
    elif role == 'Tourism Officer':
        return redirect(reverse('tourism_dash:dashboard'))
    elif role == 'Business Owner':
        return redirect(reverse('business_dash:dashboard'))
    elif role == 'Event Organizer':
        return redirect(reverse('event_dash:dashboard'))
    elif role == 'Tourist':
        return redirect(reverse('tourist_dash:dashboard'))
    else:
        # Default redirect or error page if role is not recognized
        return redirect('public-home') # Or a generic dashboard
