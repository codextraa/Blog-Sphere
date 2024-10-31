"""Signals used before or after saving a model"""
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver
from .models import User


@receiver(pre_save, sender=User)
def set_user_active(sender, instance, **kwargs):
    """Set any user to active."""
    if instance.is_active is False:
        instance.is_active = True

@receiver(post_save, sender=User)
def set_user_default_group(sender, instance, created, **kwargs):
    if created:
        default_group, _ = Group.objects.get_or_create(name="default")
        instance.groups.add(default_group)


