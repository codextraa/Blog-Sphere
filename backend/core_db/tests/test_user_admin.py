"""Tests for the Django admin modifications"""

# pylint: skip-file

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.conf import settings


class AdminSiteTests(TestCase):
    """Tests for Django admin"""

    def setUp(self):
        """Create user and client"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="Django@123",
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="test@example.com",
            password="Django@123",
        )

    def test_user_list(self):
        """Test that Users are listed on page."""
        # All the users from core_db app
        url = reverse("admin:core_db_user_changelist")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.user.email)

    def test_create_user_from_admin(self):
        """Test Creating a new user form admin interface"""

        url = reverse("admin:core_db_user_add")
        payload = {
            "email": "newuser@example.com",
            "username": "newuser@example.com",
            "slug": "newuserexamplecom",
            "password1": "Django@123",
            "password2": "Django@123",
            "is_active": True,
            "is_staff": False,
        }
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, 302)
        self.assertTrue(
            get_user_model().objects.filter(email="newuser@example.com").exists()
        )

    def test_update_user_strikes_exceeds_max(self):
        """Test that updating a user's strikes to > MAX_STRIKES fails."""
        url = reverse("admin:core_db_user_change", args=[self.user.id])
        max_strikes = getattr(settings, "MAX_STRIKES", 3)
        payload = {
            "email": self.user.email,
            "username": self.user.username,
            "slug": self.user.slug,
            "is_active": self.user.is_active,
            "is_staff": self.user.is_staff,
            "strikes": max_strikes + 1,
        }
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, 200)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.strikes, max_strikes + 1)
        self.assertContains(res, "Ensure this value is less than or equal to 3")

    def test_model_level_strikes_validation(self):
        """Test model-level validation for strikes exceeding MAX_STRIKES."""
        max_strikes = getattr(settings, "MAX_STRIKES", 3)
        user = get_user_model()(
            email="modeltest@example.com",
            password="Django@123",
            strikes=max_strikes + 1,
        )
        with self.assertRaises(ValidationError) as context:
            user.full_clean()
        self.assertIn(
            "Ensure this value is less than or equal to 3", str(context.exception)
        )
