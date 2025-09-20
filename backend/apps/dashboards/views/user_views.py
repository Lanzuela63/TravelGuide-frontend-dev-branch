# backend/apps/dashboards/views/user_views.py
from django.shortcuts import render, redirect, get_object_or_404
from apps.users.models import CustomUser
from ..forms import CustomUserForm
from django.contrib.auth.decorators import login_required, user_passes_test # New import

def is_admin(user):
    return user.is_authenticated and user.role == 'Admin' # Using CustomUser role

@login_required
@user_passes_test(is_admin)
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, "dashboards/users/user_list.html", {"users": users})

@login_required
@user_passes_test(is_admin)
def user_add(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("admin_dash:users:list")
    else:
        form = CustomUserForm()
    return render(request, "dashboards/users/user_form.html", {"form": form})

@login_required
@user_passes_test(is_admin)
def user_edit(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == "POST":
        form = CustomUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("admin_dash:users:list")
    else:
        form = CustomUserForm(instance=user)
    return render(request, "dashboards/users/user_form.html", {"form": form, "user": user})

@login_required
@user_passes_test(is_admin)
def user_delete(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == "POST":
        user.delete()
        return redirect("admin_dash:users:list")
    return render(request, "dashboards/users/user_confirm_delete.html", {"user": user})
