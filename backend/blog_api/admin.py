"""Admin registration for blog api."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Category, Blog
from .forms import CustomUserCreationForm

class UserAdmin(BaseUserAdmin):
    """Custom User Admin"""
    list_display = ('email', 'username')
    list_filter = ('groups',)
    prepopulated_fields = {"slug": ("username",)}

    #Fields to be displayed on the user detail page
    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password', 'slug')
        }),
        ('Personal_info', {
            'fields': ('first_name', 'last_name', 'phone_number', 'profile_img')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login',)
        }),
    )

    add_form = CustomUserCreationForm
    # Fields to be displayed in user creation form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'slug', 'password1', 'password2', 'is_active', 'is_staff')
        }),
    )

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_filter = ('categories',)
    prepopulated_fields = {"slug": ("title",)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)
