"""Test Cases for the User model."""
from django.test import TestCase
from blog_api.models import User, Category
from django.core.exceptions import ValidationError

class UserManagerTests(TestCase):
    def setUp(self):
        self.user_manager = User.objects

    def test_create_user_with_email_and_password(self):
        user = self.user_manager.create_user(
            email='test@example.com',
            password='SecureP@ssword123'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('SecureP@ssword123'))
        self.assertTrue(user.is_active)  # Default is_active should be False

    def test_create_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            self.user_manager.create_user(email='', password='testpass')

    def test_create_user_without_password_raises_error(self):
        with self.assertRaises(ValueError):
            self.user_manager.create_user(email='test@example.com', password='')

    def test_create_superuser(self):
        superuser = self.user_manager.create_superuser(
            email='superuser@example.com',
            password='SecureP@ssword123'
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)  # Should be True by default


class UserModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@example.com',
            password='SecureP@ssword123'
        )

    def test_string_representation(self):
        self.assertEqual(str(self.user), self.user.email)

    def test_password_validation_valid(self):
        user = User(email='valid@example.com')
        user.set_password('ValidP@ssword123')

    def test_password_validation_invalid(self):
        user = User(email='invalid@example.com')
        with self.assertRaises(ValidationError):
            user.set_password('weakpass')  # This should fail

    def test_is_active_default(self):
        self.assertTrue(self.user.is_active)  # Default value should be True

    def test_set_password_validates_on_set(self):
        user = User(email='newuser@example.com')
        user.set_password('NewValid@123')
        self.assertTrue(user.check_password('NewValid@123'))

    def test_set_password_invalid(self):
        user = User(email='user@example.com')
        with self.assertRaises(ValidationError):
            user.set_password('weakpass')  # Set a weak password


