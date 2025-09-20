# backend/apps/dashboards/views/ar_scene_views.py
from django.shortcuts import render, redirect, get_object_or_404
from apps.ar.models import ARScene
from ..forms import ARSceneForm
from django.contrib.auth.decorators import login_required, user_passes_test # New import
from django.contrib.auth import get_user_model # New import

User = get_user_model() # Get CustomUser model

def is_admin(user):
    return user.is_authenticated and user.role == 'Admin' # Using CustomUser role

@login_required
@user_passes_test(is_admin)
def ar_scene_list(request):
    scenes = ARScene.objects.all()
    return render(request, "dashboards/ar_scenes/ar_scene_list.html", {"scenes": scenes})

@login_required
@user_passes_test(is_admin)
def ar_scene_add(request):
    if request.method == "POST":
        form = ARSceneForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("admin_dash:ar_scenes:list")
    else:
        form = ARSceneForm()
    return render(request, "dashboards/ar_scenes/ar_scene_form.html", {"form": form})

@login_required
@user_passes_test(is_admin)
def ar_scene_edit(request, scene_id):
    scene = get_object_or_404(ARScene, id=scene_id)
    if request.method == "POST":
        form = ARSceneForm(request.POST, request.FILES, instance=scene)
        if form.is_valid():
            form.save()
            return redirect("admin_dash:ar_scenes:list")
    else:
        form = ARSceneForm(instance=scene)
    return render(request, "dashboards/ar_scenes/ar_scene_form.html", {"form": form, "scene": scene})

@login_required
@user_passes_test(is_admin)
def ar_scene_delete(request, scene_id):
    scene = get_object_or_404(ARScene, id=scene_id)
    if request.method == "POST":
        scene.delete()
        return redirect("admin_dash:ar_scenes:list")
    return render(request, "dashboards/ar_scenes/ar_scene_confirm_delete.html", {"scene": scene})
