"""Test cases for Category Model"""

from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from core_db.models import Category, User_Category


def create_user(email, password):
    return get_user_model().objects.create_user(email=email, password=password)


class CategoryModelTest(TestCase):
    """Test cases for Category Model"""

    def setUp(self):
        """Create a user"""
        self.user = create_user(
            email="test@example.com",
            password="Django@123",
        )

    def test_category_model(self):
        """Test category model"""
        category = Category.objects.create(
            name="Test category",
        )
        self.assertEqual(str(category), category.name)

    def test_duplicate_category_model(self):
        """Test duplicate category model"""
        Category.objects.create(
            name="Test category",
        )
        with self.assertRaises(IntegrityError):
            Category.objects.create(
                name="Test category",
            )

    def test_category_user_model(self):
        """Test category_user model"""
        category = Category.objects.create(
            name="Test category",
        )
        user_category = User_Category.objects.create(
            user=self.user,
            category=category,
        )
        self.assertEqual(str(user_category), f"{self.user.email} - {category.name}")

    def test_category_must_in_user_category_model(self):
        """Test category_user model without category"""
        with self.assertRaises(IntegrityError):
            User_Category.objects.create(
                user=self.user,
            )

    def test_user_must_in_user_category_model(self):
        """Test category_user model without user"""
        category = Category.objects.create(
            name="Test category",
        )
        with self.assertRaises(IntegrityError):
            User_Category.objects.create(
                category=category,
            )
