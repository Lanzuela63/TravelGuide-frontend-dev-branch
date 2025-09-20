# backend/apps/dashboards/views/business_views.py
from django.shortcuts import render, redirect, get_object_or_404
from apps.business.models import Business
from ..forms import BusinessForm
from django.contrib.auth.decorators import login_required, user_passes_test # Updated import

def is_admin(user):
    return user.is_authenticated and user.role == 'Admin' # Using CustomUser role

@login_required
@user_passes_test(is_admin)
def business_list(request):
    businesses = Business.objects.all()
    return render(request, "dashboards/businesses/business_list.html", {"businesses": businesses})

@login_required
@user_passes_test(is_admin)
def business_add(request):
    if request.method == "POST":
        form = BusinessForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin_dash:businesses:list")
    else:
        form = BusinessForm()
    return render(request, "dashboards/businesses/business_form.html", {"form": form})

@login_required
@user_passes_test(is_admin)
def business_edit(request, business_id):
    business = get_object_or_404(Business, id=business_id)
    if request.method == "POST":
        form = BusinessForm(request.POST, instance=business)
        if form.is_valid():
            form.save()
            return redirect("admin_dash:businesses:list")
    else:
        form = BusinessForm(instance=business)
    return render(request, "dashboards/businesses/business_form.html", {"form": form, "business": business})

@login_required
@user_passes_test(is_admin)
def business_delete(request, business_id):
    business = get_object_or_404(Business, id=business_id)
    if request.method == "POST":
        business.delete()
        return redirect("admin_dash:businesses:list")
    return render(request, "dashboards/businesses/business_confirm_delete.html", {"business": business})

@login_required
@user_passes_test(is_admin)
def admin_pending_businesses_list(request):
    pending_businesses = Business.objects.filter(is_approved=False)
    return render(request, "dashboards/businesses/admin_pending_businesses_list.html", {"businesses": pending_businesses})

@user_passes_test(is_admin) # This already has user_passes_test
def approve_business(request, business_id):
    business = get_object_or_404(Business, id=business_id)
    if request.method == "POST":
        business.is_approved = True
        business.save()
        # Optionally add a success message
        return redirect("admin_dash:pending_businesses_list")
    return redirect("admin_dash:pending_businesses_list") # Redirect if not POST