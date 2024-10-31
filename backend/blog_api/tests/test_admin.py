from django.test import TestCase
from django.contrib.admin.sites import site
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import Group
from blog_api.admin import UserAdmin

User = get_user_model()

class UserAdminTest(TestCase):
    """Test cases for the UserAdmin configuration in Django admin."""

    def setUp(self):
        """Set up test data for the UserAdmin tests."""
        # Create a test user and a group
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='Password123!'
        )
        self.group, created = Group.objects.get_or_create(name='default')

    def test_user_model_registered(self):
        """Test if User model is registered in the admin site."""
        self.assertIn(User, site._registry)
        self.assertIsInstance(site._registry[User], UserAdmin)

    def test_user_list_display(self):
        """Test that the list_display fields are correctly set."""
        user_admin = site._registry[User]
        self.assertEqual(user_admin.list_display, ('email', 'username'))

    def test_user_list_filter(self):
        """Test that the list_filter includes the 'groups' filter."""
        user_admin = site._registry[User]
        self.assertIn('groups', user_admin.list_filter)

    def test_user_fieldsets(self):
        """Test that fieldsets are set correctly for the detail page."""
        user_admin = site._registry[User]
        fieldsets = user_admin.fieldsets

        expected_fieldsets = (
            (None, {'fields': ('email', 'username', 'password')}),
            ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'profile_img')}),
            ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
            ('Important dates', {'fields': ('last_login',)}),
        )
        self.assertEqual(fieldsets, expected_fieldsets)

    def test_user_add_fieldsets(self):
        """Test that add_fieldsets are set correctly for user creation form."""
        user_admin = site._registry[User]
        add_fieldsets = user_admin.add_fieldsets

        expected_add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_staff')}
            ),
        )
        self.assertEqual(add_fieldsets, expected_add_fieldsets)

    def test_user_admin_accessible(self):
        """Test that the user admin page can be accessed by an admin user."""
        # Log in as superuser for accessing admin
        admin_user = User.objects.create_superuser(email='admin@example.com', password='AdminPass123!')
        self.client.force_login(admin_user)

        # Access the user list view in admin
        url = reverse('admin:blog_api_user_changelist')  # Replace 'app_label' with your app name
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_creation_and_edit_in_admin(self):
        """Test user creation and editing through the admin interface."""
        admin_user = User.objects.create_superuser(email='admin@example.com', password='AdminPass123!')
        self.client.force_login(admin_user)

        # Test user creation form
        url = reverse('admin:blog_api_user_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        res = self.client.post(url, {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password1': 'NewPass123!',
            'password2': 'NewPass123!',
            'is_active': True,
            'is_staff': False
        })
        self.assertEqual(res.status_code, 302)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

        # Test user editing form
        user = User.objects.get(email='newuser@example.com')
        edit_url = reverse('admin:blog_api_user_change', args=[user.id])
        res2 = self.client.post(edit_url, {
            'email': 'editeduser@example.com',
            'username': 'editeduser',
            'first_name': 'Edited',
            'last_name': 'User',
            'is_active': True,
            'is_staff': False,
            'password': 'NewPass123!'
        })

        if res2.status_code == 200:
            print("Form errors:", res2.context['adminform'].errors)

        self.assertEqual(res2.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.email, 'editeduser@example.com')
        self.assertEqual(user.first_name, 'Edited')
