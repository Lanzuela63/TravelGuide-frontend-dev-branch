#apps/users/views/auth_views.py
from allauth.socialaccount.views import SignupView
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.adapters import sociallogin_from_session
from apps.users.forms import ProfileCompletionForm
from apps.users.serializers.auth_serializers import CustomTokenObtainPairSerializer



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
    user = request.user
    role = user.groups.first().name if user.groups.exists() else "Unknown"
    return Response(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": role,
        }
    )

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

def profile_completion_view(request):
    if request.method == 'POST':
        form = ProfileCompletionForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            sociallogin = request.session.get('socialaccount_sociallogin')

            if sociallogin:
                # Deserialize sociallogin object
                sociallogin = sociallogin_from_session(request.session)
                user = sociallogin.user

                # Assign role to user
                group, _ = Group.objects.get_or_create(name=role)
                user.groups.add(group)
                user.save()

                # Log the user in
                login(request, user)
                messages.success(request, "Profile completion successful!")
                del request.session['socialaccount_sociallogin'] # Clean up session
                return redirect('public-home') # Redirect to home or dashboard
            else:
                messages.error(request, "Social login data not found in session.")
                return redirect('login') # Redirect to login if session data is missing
    else:
        form = ProfileCompletionForm()

    return render(request, 'account/profile_completion.html', {'form': form})


class CustomSocialSignupView(SignupView):
    def dispatch(self, request, *args, **kwargs):
        sociallogin = self.get_sociallogin()
        if not sociallogin.is_existing:
            # Store sociallogin in session and redirect to profile completion
            request.session['socialaccount_sociallogin'] = sociallogin.serialize()
            return redirect('profile_completion')

        # If user exists, proceed with default login
        return super().dispatch(request, *args, **kwargs)
