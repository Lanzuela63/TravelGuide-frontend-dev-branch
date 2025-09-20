# apps/tourism/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg

from .models import Review, TouristSpot, Hotel, Restaurant


def update_average_rating(instance):
    """Recalculate and update average rating for the reviewed object."""
    content_type = instance.content_type
    model_class = content_type.model_class()

    if model_class not in [TouristSpot, Hotel, Restaurant]:
        return  # only apply to models we care about

    # Get all reviews for this object
    reviews = Review.objects.filter(content_type=content_type, object_id=instance.object_id)
    avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"] or 0

    # Update the related object
    obj = model_class.objects.get(pk=instance.object_id)
    obj.average_rating = avg_rating
    obj.save(update_fields=["average_rating"])


@receiver(post_save, sender=Review)
def update_rating_on_save(sender, instance, created, **kwargs):
    update_average_rating(instance)


@receiver(post_delete, sender=Review)
def update_rating_on_delete(sender, instance, **kwargs):
    update_average_rating(instance)
