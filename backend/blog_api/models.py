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


# Create your models here.
class UserManager(BaseUserManager):
    """Custom User Manager."""

    def create_user(self, email, password, **extra_fields):
        """User Creation Manager."""
        if not email:
            raise ValueError("User must have an email address.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Superuser Creation Manager."""

        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User Model."""

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True,
                                null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True,
                                  blank=True)
    last_name = models.CharField(max_length=255, null=True,
                                 blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    profile_img = models.ImageField(upload_to="profile_images/",
                                    null=True,)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def clean(self):
        """Password verification."""
        password = self.password
        if password:
            if (len(password) < 8 or
                not re.search(r"[a-z]", password) or
                not re.search(r"[A-Z]", password) or
                not re.search(r"[0-9]", password) or
                not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
                raise ValidationError('Password must contain at least 8 characters, '
                                 'including an uppercase letter, a lowercase letter, '
                                 'a number, and a special character.')

    def is_superuser(self):
        """Check if user is superuser."""
        return self.is_staff and self.is_active

    def __str__(self):
        """Return username."""
        return self.username

