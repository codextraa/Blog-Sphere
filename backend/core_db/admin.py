# Register your models here.
"""Admin registration for blog api."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import CustomUserCreationForm, CustomBlogCreationForm
from .models import User, Category, User_Category, Blog, Blog_Category


class UserAdmin(BaseUserAdmin):
    """Custom User Admin"""

    list_display = ("email", "username")
    list_filter = ("groups",)
    prepopulated_fields = {"slug": ("username",)}

    # Fields to be displayed on the user detail page
    fieldsets = (
        (None, {"fields": ("email", "username", "password", "slug", "auth_provider")}),
        (
            "Personal_info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "bio",
                    "strikes",
                    "phone_number",
                    "profile_img",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_email_verified",
                    "is_phone_verified",
                    "is_noti_on",
                    "is_two_fa",
                    "failed_login_attempts",
                    "last_failed_login_time",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )

    add_form = CustomUserCreationForm
    # Fields to be displayed in user creation form
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "slug",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )


class BlogAdmin(admin.ModelAdmin):
    """Custom Blog Admin"""

    prepopulated_fields = {"slug": ("title",)}

    add_form = CustomBlogCreationForm


admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(User_Category)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Blog_Category)
