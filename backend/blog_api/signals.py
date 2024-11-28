"""Signals used before or after saving a model"""
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.utils.text import slugify
from .models import User, Category, Blog


@receiver(pre_save, sender=User)
def set_user_username(sender, instance, **kwargs):
    """Set unique username if not provided"""
    if not instance.username:
        instance.username = instance.email

@receiver(post_save, sender=User)
def save_user_slug(sender, instance, created, **kwargs):
    """Create slug for user using username"""
    if created or (slugify(instance.username) != instance.slug):
        instance.slug = slugify(instance.username)
        instance.save()

@receiver(post_save, sender=User)
def set_user_default_group(sender, instance, created, **kwargs):
    if created and instance.pk:
        default_group, _ = Group.objects.get_or_create(name="Default")
        instance.groups.add(default_group)

@receiver(post_save, sender=Category)
def set_category_slug(sender, instance, created, **kwargs):
    if created or (slugify(instance.name) != instance.slug):
        instance.slug = slugify(instance.name)
        instance.save()

@receiver(post_save, sender=Blog)
def set_blog_slug(sender, instance, created, **kwargs):
    if created or (slugify(instance.title) != instance.slug):
        instance.slug = slugify(instance.title)
        instance.save()


