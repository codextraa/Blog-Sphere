"""Blog Models."""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
import re


class UserManager(BaseUserManager):
    """Custom User Manager."""

    def create_user(self, email, password, **extra_fields):
        """User Creation Manager."""
        if not email:
            raise ValueError("User must have an email address.")
        if not password:
            raise ValueError("User must have a password.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # ensure password is valid
        user.save(using=self._db)

        return user

    # need to block this in production
    def create_superuser(self, email, password=None, **extra_fields):
        """Superuser Creation Manager."""
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User Model."""

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    profile_img = models.ImageField(upload_to="profile_images/", null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def _pass_valid(self, password):
        """Password verification method used when setting password"""
        if password:
            if (len(password) < 8 or
                not re.search(r"[a-z]", password) or
                not re.search(r"[A-Z]", password) or
                not re.search(r"[0-9]", password) or
                not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
                raise ValidationError('Password must contain at least 8 characters, '
                                      'including an uppercase letter, a lowercase letter, '
                                      'a number, and a special character.')

    def set_password(self, raw_password):
        """Set password and validate it."""
        self._pass_valid(raw_password)  # Ensure validation is done on set_password
        super().set_password(raw_password)

    def is_superuser(self):
        """Check if user is superuser."""
        return self.is_staff and self.is_active

    def __str__(self):
        """Return username."""
        return self.email

class Category(models.Model):
    """Category Model."""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Blog(models.Model):
    """Blog Model."""
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="blog_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.title