# backend/apps/users/adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect
from django.urls import reverse
from allauth.socialaccount.models import SocialLogin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction

User = get_user_model()


def sociallogin_from_session(session):
    data = session.get('socialaccount_sociallogin')
    if data:
        return SocialLogin.deserialize(data)
    return None


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Called right before social login is processed.
        Handles:
        - Linking social accounts to existing users (by email).
        - Redirecting new users to profile completion.
        """
        # If the social account is already linked, let allauth proceed
        if sociallogin.is_existing:
            return None

        # Try linking to an existing user by email
        email = sociallogin.user.email
        if email:
            try:
                user = User.objects.get(email=email)
                with transaction.atomic():
                    # Link the social account to the existing user
                    sociallogin.connect(request, user)
                    # Make sure the login continues with the right user
                    sociallogin.user = user
                return None  # proceed with normal login
            except User.DoesNotExist:
                pass  # No existing user found, continue below

        # No linked account, no existing user with this email → redirect to profile completion
        request.session['socialaccount_sociallogin'] = sociallogin.serialize()
        return redirect(reverse('profile_completion'))

    def save_user(self, request, sociallogin, form=None):
        """
        Saves a new social user and assigns them to the 'Tourist' group.
        """
        user = super().save_user(request, sociallogin, form)
        group, _ = Group.objects.get_or_create(name='Tourist')
        user.groups.add(group)
        user.save()
        return user

    def get_connect_redirect_url(self, request, socialaccount):
        """
        Where to redirect after a social account is connected.
        """
        return super().get_connect_redirect_url(request, socialaccount)

    def get_signup_redirect_url(self, request, socialaccount):
        """
        Where to redirect after a new social signup.
        (We override pre_social_login for profile completion.)
        """
        return super().get_signup_redirect_url(request, socialaccount)
