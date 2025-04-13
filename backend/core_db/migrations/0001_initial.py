# Generated by Django 5.1.6 on 2025-04-09 16:08

import django.core.validators
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("email", models.EmailField(max_length=255, unique=True)),
                (
                    "username",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_username",
                                message="Username cannot contain spaces",
                                regex="^\\S+$",
                            )
                        ],
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=50, null=True)),
                ("last_name", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, null=True, region=None, unique=True
                    ),
                ),
                (
                    "profile_img",
                    models.ImageField(
                        blank=True,
                        max_length=500,
                        null=True,
                        upload_to="profile_images/",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_email_verified", models.BooleanField(default=False)),
                ("is_phone_verified", models.BooleanField(default=False)),
                ("failed_login_attempts", models.IntegerField(default=0)),
                ("last_failed_login_time", models.DateTimeField(blank=True, null=True)),
                (
                    "auth_provider",
                    models.CharField(
                        choices=[
                            ("email", "Email"),
                            ("google", "Google"),
                            ("facebook", "Facebook"),
                            ("instagram", "Instagram"),
                            ("twitter", "Twitter"),
                            ("linkedin", "LinkedIn"),
                            ("github", "GitHub"),
                        ],
                        default="email",
                        max_length=20,
                    ),
                ),
                ("slug", models.SlugField(blank=True, null=True, unique=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "ordering": ["email"],
            },
        ),
    ]
