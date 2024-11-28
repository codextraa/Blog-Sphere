"""Blog Models"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re

class UserManager(BaseUserManager):
    """Custom User Manager"""

    def create_user(self, email, password, **extra_fields):
        """User Creation Manager."""
        if not email:
            raise ValueError("You must have an email address")
        if not password:
            raise ValueError("User must have a password")

        try:
            validate_email(email)
        except:
            raise ValidationError("Invalid Email format")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Super User Creation"""
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)  # Ensure is_superuser is set to True

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User class"""

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=128, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = PhoneNumberField(unique=True, blank=True, null=True)
    profile_img = models.ImageField(upload_to="profile_images/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def _pass_valid(self, password):
        """Private method for testing valid password"""
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
        """Validates raw password before hashing"""
        self._pass_valid(raw_password)
        super().set_password(raw_password)

    def save(self, *args, **kwargs):
        """Running Validators before saving"""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """Return Email"""
        return self.email

class Category(models.Model):
    """Category Model"""
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        """Running validators before saving"""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """Returns name"""
        return self.name

class Blog(models.Model):
    """Blog Model"""
    title = models.CharField(max_length=255)
    content = models.TextField()
    blog_image = models.ImageField(upload_to="blog_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        """Running validators before saving"""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """Returns title"""
        return self.title