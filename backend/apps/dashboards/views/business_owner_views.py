# backend/apps/dashboards/views/business_owner_views.py
from django.shortcuts import render, redirect, get_object_or_404
from apps.business.models import Business
from ..forms import BusinessForm
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.contrib.auth.decorators import login_required, user_passes_test # New import
from django.contrib.auth import get_user_model # New import

User = get_user_model() # Get CustomUser model

def is_business_owner(user):
    return user.is_authenticated and user.role == 'Business Owner'

@login_required
@user_passes_test(is_business_owner)
def business_owner_dashboard(request):
    user_businesses = Business.objects.filter(owner=request.user) # Filter once
    
    my_businesses_count = user_businesses.count()
    pending_businesses_count = user_businesses.filter(is_approved=False).count()
    total_approved_businesses = my_businesses_count - pending_businesses_count

    # Data for Approval Status Pie Chart
    approved_count = user_businesses.filter(is_approved=True).count()
    pending_count = user_businesses.filter(is_approved=False).count()
    
    approval_chart_data = {
        "labels": ["Approved", "Pending"],
        "data": [approved_count, pending_count],
    }

    # Data for Business Creation Trend Line Chart
    creation_trend = user_businesses.annotate(month=TruncMonth('created_at')) \
                                    .values('month') \
                                    .annotate(count=Count('id')) \
                                    .order_by('month')
    
    creation_chart_labels = [month['month'].strftime('%Y-%m') for month in creation_trend]
    creation_chart_data = [month['count'] for month in creation_trend]

    context = {
        "welcome_message": f"Welcome, {request.user.first_name}!",
        "my_businesses_count": my_businesses_count,
        "pending_businesses_count": pending_businesses_count,
        "total_approved_businesses": total_approved_businesses,
        "latest_businesses": user_businesses.order_by('-created_at')[:5], # Latest 5 businesses
        "approval_chart_data": approval_chart_data,
        "creation_chart_labels": creation_chart_labels,
        "creation_chart_data": creation_chart_data,
    }
    return render(request, "dashboards/business_owner_dashboard.html", context)

@login_required
@user_passes_test(is_business_owner)
def business_owner_business_list(request):
    businesses = Business.objects.filter(owner=request.user)
    return render(request, "dashboards/businesses/business_owner_business_list.html", {"businesses": businesses})

@login_required
@user_passes_test(is_business_owner)
def business_owner_business_add(request):
    if request.method == "POST":
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.owner = request.user # Assign current user as owner
            business.save()
            return redirect("business_owner_dash:business_list")
    else:
        form = BusinessForm(initial={'owner': request.user})
    return render(request, "dashboards/businesses/business_owner_business_form.html", {"form": form})

@login_required
@user_passes_test(is_business_owner)
def business_owner_business_edit(request, business_id):
    business = get_object_or_404(Business, id=business_id, owner=request.user)
    if request.method == "POST":
        form = BusinessForm(request.POST, request.FILES, instance=business)
        if form.is_valid():
            form.save()
            return redirect("business_owner_dash:business_list")
    else:
        form = BusinessForm(instance=business)
    return render(request, "dashboards/businesses/business_owner_business_form.html", {"form": form, "business": business})

@login_required
@user_passes_test(is_business_owner)
def business_owner_business_delete(request, business_id):
    business = get_object_or_404(Business, id=business_id, owner=request.user)
    if request.method == "POST":
        business.delete()
        return redirect("business_owner_dash:business_list")
    return render(request, "dashboards/businesses/business_owner_business_confirm_delete.html", {"business": business})