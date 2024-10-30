"""Signals used before or after saving a model"""
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import User


@receiver(pre_save, sender=User)
def set_user_active(sender, instance, **kwargs):
    """Set any user to active."""
    if instance.is_active is False:
        instance.is_active = True

