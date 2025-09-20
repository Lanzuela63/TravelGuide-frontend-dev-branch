#apps/users/urls.py
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from apps.users.views.api_views import LogoutAPIView, RegisterAPIView, UserProfileUpdateAPIView, CustomLoginView # Added CustomLoginView
from apps.users.views.auth_views import (
    profile_completion_view, CustomSocialSignupView, user_profile_view # Only profile_completion_view
)
from django.urls import path
from .views.main_views import public_home, dashboard_redirect_view
from . import views
from .views import profile_views
from .views.profile_views import edit_profile

urlpatterns = [

    path('profile-completion/', profile_completion_view, name='profile_completion'), # Added profile_completion path
    path('', public_home, name='index'),
    path('', views.public_home, name='public-home'),
    path('dashboard/', dashboard_redirect_view, name='dashboard_redirect'),
    path('api/profile/update/', UserProfileUpdateAPIView.as_view(), name='api-profile-update'),

        # Web Auth

    # API Auth
    path('api/auth/register/', RegisterAPIView.as_view(), name='api-register'),
    path('api/auth/token/', CustomLoginView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/auth/me/', user_profile_view, name='user-profile'),
    path('api/auth/logout/', LogoutAPIView.as_view(), name='api-logout'),

    # Profile Edit
    path('profile/', profile_views.view_profile, name='view_profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),

    # Override allauth social signup
    path('social/signup/', CustomSocialSignupView.as_view(), name='socialaccount_signup'),

]