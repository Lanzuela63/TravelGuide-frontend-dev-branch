#apps/ar/api_urls.py
from django.urls import path
from .views import api_views

app_name = "ar_api"

urlpatterns = [
    path("scenes/", api_views.list_ar_scenes, name="list_scenes"),
    path("scenes/nearby/", api_views.nearby_ar_scenes, name="nearby_ar_scenes"),
    path("test/", api_views.test_ar_api, name="test_ar_api"),
]
