"""Admin forms."""

import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Blog


User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """User Creation Form."""

    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")

    def clean(self):
        """Custom validation."""
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if not email:
            raise ValidationError("Email is required.")

        if not username:
            raise ValidationError("Username is required.")

        if not password1:
            raise ValidationError("Password is required.")

        if password1 != password2:
            raise ValidationError("Passwords do not match.")

        if (
            len(username) < 6
            or len(username) > 255
            or " " in username
            or not re.match(r"^[a-zA-Z0-9._@-]+$", username)
        ):
            raise ValidationError(
                "Username must be at least 6 characters long. "
                "Username cannot be longer than 255 characters. "
                "Username cannot contain spaces. "
                "Username can only contain letters, numbers, "
                "periods, underscores, hyphens, and @ signs."
            )

        if (  # pylint: disable= R0801
            len(password1) < 8
            or not re.search(r"[a-z]", password1)
            or not re.search(r"[A-Z]", password1)
            or not re.search(r"[0-9]", password1)
            or not re.search(r"[!@#$%^&*(),.?\":{}|<>[\]~/\\']", password1)
        ):
            raise ValidationError(
                "Password must contain at least 8 characters, "
                "including an uppercase letter, a lowercase letter, "
                "a number, and a special character."
            )

        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists.")

        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")

        return cleaned_data


class CustomBlogCreationForm(forms.ModelForm):
    """Blog Creation form."""

    class Meta:
        model = Blog
        fields = (
            "title",
            "content",
            "overview",
            "author",
            "likes",
            "cat_count",
            "report_count",
            "status",
            "visibility",
            "score",
            "slug",
        )
        widgets = {
            "author": forms.Select(),
            "status": forms.Select(),
            "content": forms.Textarea(attrs={"rows": 10, "cols": 40}),
            "visibility": forms.CheckboxInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        overview = cleaned_data.get("overview")
        content = cleaned_data.get("content")
        cat_count = cleaned_data.get("cat_count")

        if len(title) < 10:
            raise ValidationError("Title must be at least 10 characters long.")
        if len(title) > 100:
            raise ValidationError("Title cannot be longer than 100 characters.")
        if len(overview) < 20:
            raise ValidationError("Overview must be at least 20 characters long.")
        if len(overview) > 150:
            raise ValidationError("Overview cannot be longer than 150 characters.")
        if len(content) < 100:
            raise ValidationError("Content must be at least 100 characters long.")
        if cat_count > 5:
            raise ValidationError("Cannot add more than 5 categories.")

        return cleaned_data
