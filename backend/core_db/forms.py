"""Admin forms."""

import re
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


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
