from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from django import forms
from apps.users.models import CustomUser
from allauth.account.forms import SignupForm # Import SignupForm
from django.contrib.auth.models import Group # Import Group


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'profile_image']

class ProfileCompletionForm(forms.Form):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)

class CustomSignupForm(SignupForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        role = self.cleaned_data['role']
        group, _ = Group.objects.get_or_create(name=role)
        user.groups.add(group)
        user.save()
        return user