from django.test import TestCase
from blog_api.models import User
from blog_api.serializers import UserSerializer

class UserSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '+8801912345678',
            'profile_img': None,  # Assuming profile_img is optional
            'password': 'Password123!'
        }

        # self.user = User.objects.create_superuser(email='admin@example.com', password='AdminPass123!')
        # self.serializer = UserSerializer()

    def test_user_creation(self):
        """Test creating a user with valid data."""
        serializer = UserSerializer(data=self.valid_data)
        if not serializer.is_valid():
            print(serializer.errors)

        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertEqual(user.email, self.valid_data['email'])
        self.assertTrue(user.check_password(self.valid_data['password']))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_user_creation_invalid_email(self):
        """Test creating a user with invalid email."""
        invalid_data = self.valid_data.copy()
        invalid_data['email'] = 'invalid-email'

        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_user_update(self):
        """Test updating a user."""
        user = User.objects.create_user(**self.valid_data)
        update_data = {
            'email': 'updateduser@example.com',
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User',
            'phone_number': '+8801913452678',
            'profile_img': None,
            'password': 'NewPassword123!'
        }

        serializer = UserSerializer(instance=user, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()

        self.assertEqual(updated_user.email, update_data['email'])
        self.assertTrue(updated_user.check_password(update_data['password']))
        self.assertEqual(updated_user.first_name, update_data['first_name'])
        self.assertEqual(updated_user.phone_number, update_data['phone_number'])

    def test_user_update_no_password_change(self):
        """Test updating a user without changing the password."""
        user = User.objects.create_user(**self.valid_data)
        update_data = {
            'email': 'updateduser@example.com',
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User',
            'profile_img': None,
        }
        serializer = UserSerializer(instance=user, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()

        self.assertEqual(updated_user.email, update_data['email'])
        self.assertEqual(updated_user.first_name, update_data['first_name'])
        self.assertEqual(updated_user.phone_number, self.valid_data['phone_number'])
        self.assertTrue(updated_user.check_password(self.valid_data['password']))

