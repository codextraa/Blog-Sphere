"""Tests for the Django admin modifications"""

# pylint: skip-file

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.conf import settings
from core_db.models import Category, User_Category, Blog, Blog_Category

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_admin_user(email="admin@example.com", password="Django@123"):
    """Create and return a new superuser"""
    return get_user_model().objects.create_superuser(email=email, password=password)


class UserAdminSiteTests(TestCase):
    """Tests for Django admin User"""

    def setUp(self):
        """Create user and client"""
        self.client = Client()
        self.admin_user = create_admin_user()
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


class CategoryAdminSiteTests(TestCase):
    """Tests for Django admin Category"""

    def setUp(self):
        """Create user and client"""
        self.client = Client()
        self.admin_user = create_admin_user()
        self.client.force_login(self.admin_user)
        self.category = Category.objects.create(name="Test Category")
        self.user_category = User_Category.objects.create(
            user=self.admin_user, category=self.category
        )

    def test_category_list(self):
        """Test that Categories are listed on page."""
        # All the categories from core_db app
        url = reverse("admin:core_db_category_changelist")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.category.name)

    def test_create_category_from_admin(self):
        """Test Creating a new category form admin interface"""

        url = reverse("admin:core_db_category_add")
        payload = {
            "name": "newcategory",
        }
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, 302)
        self.assertTrue(Category.objects.filter(name="newcategory").exists())

    def test_create_user_category_from_admin(self):
        """Test Creating a new user_category form admin interface"""

        url = reverse("admin:core_db_user_category_add")
        payload = {
            "user": self.admin_user,
            "category": self.category,
        }
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(
            User_Category.objects.filter(
                user=self.admin_user, category=self.category
            ).exists()
        )


class BlogAdminSiteTests(TestCase):
    """Tests for Django admin Blog"""

    def setUp(self):
        """Create user and client"""
        self.client = Client()
        self.admin_user = create_admin_user()
        self.client.force_login(self.admin_user)
        self.category = Category.objects.create(name="Test Category")
        self.user_category = User_Category.objects.create(
            user=self.admin_user, category=self.category
        )

    def test_blog_list(self):
        """Test that Blogs are listed on page."""
        # All the categories from core_db app
        url = reverse("admin:core_db_blog_changelist")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_blog_from_admin(self):
        """Test that Creating a new blog from admin interface"""
        url = reverse("admin:core_db_blog_add")
        payload = {
            "title": "Test Blog Title",
            "author": self.admin_user.id,
            "overview": "o" * 21,
            "content": "c" * 101,
            "likes": 0,
            "cat_count": 0,
            "report_count": 0,
            "status": "Draft",
            "_save": "",
        }
        res = self.client.post(url, payload, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(
            Blog.objects.filter(title="Test Blog Title").exists(),
        )

    def test_create_blog_category_from_admin(self):
        """Test Creating a new blog_category from admin interface"""
        blog = Blog.objects.create(
            title="Test Blog Title",
            author=self.admin_user,
            overview="o" * 21,
            content="c" * 101,
            likes=0,  # Add required fields
            cat_count=0,
            report_count=0,
            status="Draft",
        )
        url = reverse("admin:core_db_blog_category_add")
        payload = {
            "blog": blog.id,
            "category": self.category.id,
            "_save": "",
        }
        res = self.client.post(url, payload, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(
            Blog_Category.objects.filter(blog=blog, category=self.category).exists(),
        )
