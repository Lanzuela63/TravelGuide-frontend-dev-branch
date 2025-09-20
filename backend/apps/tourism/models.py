# apps/tourism/models.py
from django.conf import settings
from django.utils.text import slugify
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _
from django.core.validators import MinValueValidator, MaxValueValidator


# -------------------------------
# Province, City, Barangay
# -------------------------------
class Province(models.Model):
    psgc_code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CityMunicipality(models.Model):
    psgc_code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="cities")

    def __str__(self):
        return f"{self.name}, {self.province.name}"


class Barangay(models.Model):
    psgc_code = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=150)
    city = models.ForeignKey(CityMunicipality, on_delete=models.CASCADE, related_name="barangays")

    def __str__(self):
        return f"{self.name}, {self.city.name}"


# -------------------------------
# Base Location
# -------------------------------
class BaseLocation(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)   # ✅ ADD HERE
    description = models.TextField(blank=True, null=True)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(CityMunicipality, on_delete=models.SET_NULL, null=True, blank=True)
    barangay = models.ForeignKey(Barangay, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='locations/', default='locations/default.jpg')
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    show_in_carousel = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.city.name}, {self.province.name}"


# -------------------------------
# Main Location Types
# -------------------------------
class TouristSpot(BaseLocation):
    entrance_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    operating_hours = models.CharField(max_length=100, null=True, blank=True)
    contact_number = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(_("Email address"), max_length=254)
    website = models.URLField(null=True, blank=True)
    average_rating = models.FloatField(default=0.0)   # ✅ ratings
    categories = GenericRelation("CategorizedItem", related_query_name="tourist_spot")
    ratings = GenericRelation("Review", related_query_name="tourist_spot_reviews")
    


class Hotel(BaseLocation):
    stars = models.IntegerField(
        choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
        default=3
    )
    amenities = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    average_rating = models.FloatField(default=0.0)   # ✅ ratings
    categories = GenericRelation("CategorizedItem", related_query_name="hotel")


class Restaurant(BaseLocation):
    cuisine_type = models.CharField(max_length=100, blank=True, null=True)
    average_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    contact_number = models.CharField(max_length=50, blank=True, null=True)
    average_rating = models.FloatField(default=0.0)   # ✅ ratings
    categories = GenericRelation("CategorizedItem", related_query_name="restaurant")


# -------------------------------
# Reviews & Related Models
# -------------------------------
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Generic relation fields
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    location = GenericForeignKey("content_type", "object_id")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.rating}⭐"


class Gallery(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    location = GenericForeignKey('content_type', 'object_id')
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'Image of {self.location.name}'


class OperatingHour(models.Model):
    DAYS_OF_WEEK = [
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    ]

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    location = GenericForeignKey('content_type', 'object_id')
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK, default='Mon')
    open_time = models.TimeField()
    close_time = models.TimeField()

    def __str__(self):
        return f'{self.location.name} - {self.get_day_of_week_display()}'


# -------------------------------
# User Saved/Visited
# -------------------------------
class SavedSpot(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    spot = models.ForeignKey("TouristSpot", on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} saved {self.spot}"


class VisitedSpot(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    spot = models.ForeignKey("TouristSpot", on_delete=models.CASCADE)
    visited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} visited {self.spot}"


# -------------------------------
# Categories
# -------------------------------
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        app_label = 'tourism'
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class CategorizedItem(models.Model):
    """
    Generic link between Category and any location-type model (TouristSpot, Hotel, Restaurant).
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        unique_together = ('category', 'content_type', 'object_id')

    def __str__(self):
        return f"{self.content_object} → {self.category.name}"
