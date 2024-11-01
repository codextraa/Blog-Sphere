from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from blog_api.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class UserViewSetTestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "+8801912345678",
            "password": "Password123!"
        }
        self.user = User.objects.create_user(**self.user_data)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_token(self.user))
        self.url = reverse("user-list")  # Adjust this name to match your URL patterns

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_create_user(self):
        """Test creating a user."""
        response = self.client.post(self.url, data={
            "email": "newuser@example.com",
            "username": "newuser",
            "first_name": "New",
            "last_name": "User",
            "phone_number": "+8801912345678",
            "password": "NewPassword123!"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertIn("id", response.data)
        self.assertNotEqual(response.data["password"], "NewPassword123!")  # Password should be hashed

    def test_retrieve_user(self):
        """Test retrieving user details with authentication."""
        response = self.client.get(reverse("user-detail", args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user_data["email"])

    def test_update_user(self):
        """Test updating user details with authentication."""
        update_data = {
            "first_name": "Updated",
            "last_name": "UserUpdated"
        }
        response = self.client.patch(reverse("user-detail", args=[self.user.id]), data=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, update_data["first_name"])
        self.assertEqual(self.user.last_name, update_data["last_name"])

    def test_delete_user(self):
        """Test deleting a user with authentication."""
        response = self.client.delete(reverse("user-detail", args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())