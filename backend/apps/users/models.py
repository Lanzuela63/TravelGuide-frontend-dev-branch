from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


def user_profile_upload_path(instance, filename):
    return f'profile_images/user_{instance.id}/{filename}'

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('Tourist', 'Tourist'),
        ('Tourism Officer', 'Tourism Officer'),
        ('Business Owner', 'Business Owner'),
        ('Event Organizer', 'Event Organizer'),
        ('Admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Tourist')
    profile_image = models.ImageField(upload_to=user_profile_upload_path, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",
        related_query_name="user",
    )

    def __str__(self):
        return f"{self.username} ({self.role})"