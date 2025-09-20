from django.db import models
from django.contrib.auth import get_user_model
from apps.tourism.models import CityMunicipality # New import

User = get_user_model()

class BusinessCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Business Categories"

    def __str__(self):
        return self.name

class Business(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255, blank=True, null=True) # New field
    city = models.ForeignKey(CityMunicipality, on_delete=models.SET_NULL, blank=True, null=True) # New field
    latitude = models.FloatField(blank=True, null=True) # New field
    longitude = models.FloatField(blank=True, null=True) # New field
    phone_number = models.CharField(max_length=20, blank=True, null=True) # New field
    email = models.EmailField(blank=True, null=True) # New field
    website = models.URLField(blank=True, null=True) # New field
    category = models.ForeignKey(BusinessCategory, on_delete=models.SET_NULL, blank=True, null=True) # New field
    logo = models.ImageField(upload_to='business_logos/', blank=True, null=True) # New field
    cover_image = models.ImageField(upload_to='business_cover_images/', blank=True, null=True) # New field
    opening_hours = models.CharField(max_length=255, blank=True, null=True) # New field
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
