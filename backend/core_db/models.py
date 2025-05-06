"""Blog User Model"""

import re
import secrets
import string
from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.core.validators import (
    validate_email,
    MaxValueValidator,
)
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    """Custom User Manager"""

    def create_user(self, email, password=None, **extra_fields):
        """Custom User Creation"""
        if not email:
            raise ValueError("You must have an email address")

        try:
            validate_email(email)
        except ValidationError as exc:
            raise ValidationError("Invalid Email Format") from exc

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
            user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Super User Creation"""
        if not password:
            raise ValueError("SuperUser must have a password")

        extra_fields.setdefault("is_email_verified", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User Class"""

    class Meta:
        ordering = ["email"]

    AUTH_PROVIDER = [
        ("email", "Email"),
        ("google", "Google"),
        ("facebook", "Facebook"),
        ("github", "GitHub"),
    ]
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
    )
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    bio = models.CharField(blank=True, null=True, max_length=150)
    phone_number = PhoneNumberField(unique=True, blank=True, null=True)
    profile_img = models.ImageField(
        upload_to="profile_images/", blank=True, null=True, max_length=500
    )
    strikes = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(getattr(settings, "MAX_STRIKES", 3))],
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    is_noti_on = models.BooleanField(default=True)
    is_two_fa = models.BooleanField(default=True)
    failed_login_attempts = models.IntegerField(default=0)
    last_failed_login_time = models.DateTimeField(blank=True, null=True)
    auth_provider = models.CharField(
        max_length=20, choices=AUTH_PROVIDER, default="email"
    )
    slug = models.SlugField(unique=True, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def _username_valid(self, username):
        """Private method for testing valid username"""
        if username:
            if len(username) < 6:
                raise ValidationError("Username must be at least 6 characters long.")
            if len(username) > 255:
                raise ValidationError("Username cannot be longer than 255 characters.")
            if " " in username:
                raise ValidationError("Username cannot contain spaces.")
            if not re.match(r"^[a-zA-Z0-9._@-]+$", username):
                raise ValidationError(
                    "Username can only contain letters, numbers, "
                    "periods, underscores, hyphens, and @ signs."
                )

    def _pass_valid(self, password):
        """Private method for testing valid password"""
        if password:
            if (
                len(password) < 8
                or not re.search(r"[a-z]", password)
                or not re.search(r"[A-Z]", password)
                or not re.search(r"[0-9]", password)
                or not re.search(r"[!@#$%^&*(),.?\":{}|<>[\]~/\\']", password)
            ):
                raise ValidationError(
                    "Password must contain at least 8 characters, "
                    "including an uppercase letter, a lowercase letter, "
                    "a number, and a special character."
                )

    @staticmethod
    def create_random_password(length=16):
        """
        Generate a cryptographically secure random password of the given length.
        Ensures at least one uppercase letter, one lowercase letter, one digit,
        and one special character are included in the password.
        """
        if length < 4:
            raise ValueError(
                "Password length must be at least 4 characters to meet the requirements"
            )

        # Define the character sets
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        digits = string.digits
        punctuation = string.punctuation

        # Ensure at least one of each character type
        password = [
            secrets.choice(lower),
            secrets.choice(upper),
            secrets.choice(digits),
            secrets.choice(punctuation),
        ]

        # Fill the rest of the password length with random characters from all sets
        alphabet = lower + upper + digits + punctuation
        password += [secrets.choice(alphabet) for _ in range(length - 4)]

        # Shuffle the password to mix the characters
        secrets.SystemRandom().shuffle(password)

        return "".join(password)

    def set_password(self, raw_password):
        """Validates raw password before hashing"""
        self._pass_valid(raw_password)
        super().set_password(raw_password)

    def save(self, *args, **kwargs):
        """Running Validators before saving"""
        self._username_valid(self.username)
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """Return Email"""
        return f"{self.email}"


class Category(models.Model):
    """Category Model"""

    name = models.CharField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        """Running Validators before saving"""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class User_Category(models.Model):
    """User Category Model"""

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "category"], name="unique_user_category"
            )
        ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """Running Validators before saving"""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} - {self.category.name}"


class Blog(models.Model):
    """Blog Model"""

    STATUS = (
        ("Draft", "Draft"),
        ("Published", "Published"),
    )

    title = models.CharField(max_length=100)
    content = models.TextField()
    overview = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    cat_count = models.IntegerField(default=0)
    report_count = models.IntegerField(default=0)
    status = models.CharField(max_length=12, choices=STATUS, default="Draft")
    visibility = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(default=0.0)
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["-score"]),
            models.Index(fields=["-created_at"]),
            models.Index(fields=["status", "visibility", "-score"]),
        ]

    def _blog_validation(self):
        if len(self.title) < 10:
            raise ValidationError("Title must be at least 10 characters long.")
        if len(self.title) > 100:
            raise ValidationError("Title cannot be longer than 100 characters.")
        if len(self.overview) < 20:
            raise ValidationError("Overview must be at least 20 characters long.")
        if len(self.overview) > 150:
            raise ValidationError("Overview cannot be longer than 150 characters.")
        if len(self.content) < 100:
            raise ValidationError("Context must be at least 100 characters long.")
        if self.cat_count > 5:
            raise ValidationError("Cannot add more than 5 categories.")

    def save(self, *args, **kwargs):
        """Running Validators before saving"""
        self._blog_validation()
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"


class Blog_Category(models.Model):
    """Blog Category Model"""

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["blog", "category"], name="unique_blog_category"
            )
        ]

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """Running Validators before saving"""
        self.full_clean()
        if self.blog.cat_count >= 5:
            raise ValidationError("Cannot add more than 5 categories.")

        self.blog.cat_count += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.blog.title} - {self.category.name}"
