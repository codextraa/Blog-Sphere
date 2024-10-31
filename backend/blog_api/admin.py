"""Admin registration for blog api."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


# Register your models here.
class UserAdmin(BaseUserAdmin):
    """Custom User Admin."""
    list_display = ('email', 'username')
    list_filter = ('groups',)

    # Fields to be displayed on the user detail page
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'profile_img')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')
        }),
        ('Important dates', {'fields': ('last_login',)}),
    )

    # Fields to be displayed in the user creation form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )


admin.site.register(User, UserAdmin)