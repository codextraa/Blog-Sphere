"""Test Cases for User"""
import os, io
from django.conf import settings
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions  import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class UserModelTests(TestCase):
    """Test User Model"""

    def test_create_user_with_email(self):
        """Test Creating a user with an email is successful"""
        email = 'test@example.com'
        password = 'Django@123'
        user = get_user_model().objects.create_user(
            email = email,
            password = password,
        )

        default_group = Group.objects.get(name="Default")
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertEqual(user.username, email) # checking if username signal is working
        self.assertIn(default_group, user.groups.all()) # checking if group signal is working

    def test_create_user_without_valid_email(self):
        """Test Creating a user without a proper email"""
        email = 'test'
        password = 'Django@123'

        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(
                email = email,
                password=password,
            )

    def test_create_user_without_valid_password(self):
        """Test Creating a user without a proper password"""
        email = 'test@example.com'
        password = 'testpass'

        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(
                email = email,
                password=password,
            )

    def test_create_user_without_email_password(self):
        """Test Creating a user without email or password"""
        email = ''
        password = ''

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email = email,
                password=password,
            )

    def test_create_superuser_with_valid_data(self):
        """Test creating a superuser with valid data"""
        email = "superuser@example.com"
        password = "Superuser@123"

        # Create superuser
        superuser = get_user_model().objects.create_superuser(email=email, password=password)

        # Check that the superuser was created correctly
        self.assertEqual(superuser.email, email)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)

    def test_create_superuser_without_is_staff(self):
        """Test creating a superuser without is_staff"""
        email = "superuser@example.com"
        password = "Superuser@123"

        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(
                email=email,
                password=password,
                is_staff=False # Set to false to trigger ValueError
            )

    def test_create_superuser_without_is_superuser(self):
        """Test creating a superuser without is_staff"""
        email = "superuser@example.com"
        password = "Superuser@123"

        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(
                email=email,
                password=password,
                is_superuser=False # Set to false to trigger ValueError
            )

    def test_user_with_valid_phone_number(self):
        """Test creating a user with a valid phone number"""
        email = 'test@example.com'
        password = 'Django@123'
        phone_number = '+8801999999999'

        user = get_user_model().objects.create_user(
            email = email,
            password = password,
            phone_number = phone_number
        )

        self.assertEqual(user.phone_number, phone_number)

    def test_user_with_invalid_phone_number(self):
        """Test creating a user with an invalid phone number"""
        email = 'test@example.com'
        password = 'Django@123'
        phone_number = '12345' # Invalid phone number

        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(
                email = email,
                password = password,
                phone_number = phone_number
            )

    def test_creating_user_slug(self):
        """Test creating a user with a slug"""
        email = 'test@example.com'
        password = 'Django@123'
        slug = 'testexamplecom'

        user = get_user_model().objects.create_user(
            email = email,
            password = password,
        )

        self.assertEqual(user.slug, slug)

    def test_user_slug_with_username_assigned(self):
        """Test creating a user with a slug"""
        email = 'test@example.com'
        password = 'Django@123'
        username = 'test user'
        slug = 'test-user'

        user = get_user_model().objects.create_user(
            email = email,
            password = password,
            username = username
        )

        self.assertEqual(user.slug, slug)

    def test_user_slug_update_with_username_update(self):
        """Test creating a user with a slug"""
        email = 'test@example.com'
        password = 'Django@123'
        slug = 'test-user'

        user = get_user_model().objects.create_user(
            email = email,
            password = password,
        )

        user.username = 'test user'
        user.save()

        self.assertEqual(user.slug, slug)


class UserModelImageTests(TestCase):
    """Testing Image upload."""

    def setUp(self):
        "Environment Setup"
        # Create a 10x10 black image using Pillow
        black_image = Image.new("RGB", (10, 10), "black")

        # Save the image to BytesIO object
        image_bytes = io.BytesIO()
        black_image.save(image_bytes, format="JPEG")
        image_bytes.seek(0)

        # Create the image
        self.image = SimpleUploadedFile(
            name="test_image.jpg",
            content=image_bytes.read(),
            content_type="image/jpeg",
        )

        #Create the User
        self.user = get_user_model().objects.create_user(
            email="test@example.com",
            password="Django@123",
        )

    def tearDown(self):
        if os.path.exists(self.image_path):
            os.remove(self.image_path)
        self.user.delete()

    def test_user_with_profile_image(self):
        """Test creating a user with a profile image"""
        self.user.profile_img = self.image
        self.user.save()
        self.image_path = os.path.join(settings.MEDIA_ROOT, self.user.profile_img.name)

        self.assertTrue(self.user.profile_img)
        self.assertEqual(self.user.profile_img.name, "profile_images/test_image.jpg")
        self.assertTrue(os.path.exists(self.image_path))


USER_URL = reverse('user-list') # get/post
TOKEN_USER_URL = reverse('token_obtain_pair') # token
TOKEN_REFRESH_URL = reverse('token_refresh') # token refresh

def detail_url(user_id):
    """Create and return a user detail URL"""
    return reverse('user-detail', args=[user_id])

def image_upload_url(user_id):
    """Create and return a user image upload URL"""
    return reverse('user-upload-image', args=[user_id])

def deactivate_user_url(user_id):
    """Deactivate user URL"""
    return reverse('user-deactivate-user', args=[user_id])

def activate_user_url(user_id):
    """Activate user URL"""
    return reverse('user-activate-user', args=[user_id])

def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(APITestCase):
    """Test the public feature of user API"""

    def setUp(self):
        self.client = APIClient() # http request simulation

    def test_create_user_success(self):
        """Test creating a user is successful"""
        payload = {
            'email': 'test@example.com',
            'password': 'Django@123'
        }

        res = self.client.post(USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

        default_image_path = 'profile_images/default_profile.jpg'
        self.assertEqual(user.profile_img.name, default_image_path)

    def test_user_with_email_exist_error(self):
        """Test error returned if user with email exists"""
        payload = {
            "email": "test@example.com",
            "password": "Django@123",
        }
        create_user(**payload)
        res = self.client.post(USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_with_invalid_password(self):
        """Test error returned if password is invalid"""
        payload = {
            "email": "test@example.com",
            "password": "Django",
        }
        with self.assertRaises(ValidationError):
            self.client.post(USER_URL, payload)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Create token for user"""
        user_details = {
            'email': 'test@example.com',
            'password': 'Django@123',
        }

        create_user(**user_details)
        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)
        self.assertIn("refresh", res.data)

    def test_create_new_access_token_with_refresh_token(self):
        """Create new access token with refresh token"""
        user_details = {
            'email': 'test@example.com',
            'password': 'Django@123',
        }

        create_user(**user_details)
        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        token_res = self.client.post(TOKEN_USER_URL, payload)

        self.assertEqual(token_res.status_code, status.HTTP_200_OK)
        self.assertIn('access', token_res.data)
        self.assertIn('refresh', token_res.data)

        refresh_payload = {
            'refresh': token_res.data['refresh'],
        }
        refresh_res = self.client.post(TOKEN_REFRESH_URL, refresh_payload)

        self.assertEqual(refresh_res.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_res.data)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        user_details = {
            'email': 'test@example.com',
            'password': 'Django@123',
        }
        create_user(**user_details)
        payload = {
            'email': user_details['email'],
            'password': 'badpass',
        }
        res = self.client.post(TOKEN_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('token', res.data)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for user list retrieval"""
        res = self.client.get(USER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(APITestCase):
    """Private user API tests"""
    def setUp(self):
        """Environment setup"""
        self.user = create_user(
            email = 'test@example.com',
            password = 'Django@123',
            first_name = 'test name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user) # simulating authentication

    def test_retrieve_user_successful(self):
        """Test retrieving a list of users"""
        res = self.client.get(USER_URL) # returns a list of the users
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]['email'], self.user.email)

    def test_post_user_not_allowed(self):
        """Test that POST is not allowed on the user endpoint"""
        res = self.client.post(USER_URL, {}) # can't create user if logged in
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {
            'first_name': 'new name',
            'password': 'Djangonew@123'
        }
        url = detail_url(self.user.id)
        res = self.client.patch(url, payload)
        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.first_name, payload['first_name'])
        self.assertTrue(self.user.check_password(payload['password']))

    def test_update_user_profile_as_superuser(self):
        """Test updating the user profile for superuser"""
        superuser = get_user_model().objects.create_superuser(
            email = 'admin@example.com',
            password = 'Django@123',
        )
        self.client.force_authenticate(user=superuser)

        payload = {
            'first_name': 'new name',
            'password': 'Djangonew@123'
        }
        url = detail_url(self.user.id)
        res = self.client.patch(url, payload)
        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.first_name, payload['first_name'])
        self.assertTrue(self.user.check_password(payload['password']))

    def test_cannot_update_user_profile_as_staff(self):
        """Test updating the user profile for staff user"""
        staff_user = create_user(
            email = 'staff@example.com',
            password = 'Django@123',
            is_staff = True
        )
        self.client.force_authenticate(user=staff_user)

        payload = {
            'first_name': 'new name',
            'password': 'Djangonew@123'
        }
        url = detail_url(self.user.id)
        res = self.client.patch(url, payload)
        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_update_is_active(self):
        """Cannot update is_active field"""
        payload = {
            'is_active': False,
        }
        url = detail_url(self.user.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_own_user_profile(self):
        """Normal user cannot delete thier profile"""
        url = detail_url(self.user.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_staff_other_user_profile(self):
        """Staff user cannot delete other user profile"""
        staff_user = create_user(
            email = 'staff@example.com',
            password = 'Django@123',
            is_staff = True
        )
        self.client.force_authenticate(user=staff_user)

        url = detail_url(self.user.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_delete_other_user_profile(self):
        """Delete another user profile for superuser"""
        superuser = get_user_model().objects.create_superuser(
            email = 'admin@example.com',
            password = 'Django@123',
        )
        self.client.force_authenticate(user=superuser)

        url = detail_url(self.user.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        exists = get_user_model().objects.filter(
            id=self.user.id
        ).exists()
        self.assertFalse(exists)

    def test_superuser_cannot_delete_superuser(self):
        """Delete superuser profile for superuser"""
        superuser = get_user_model().objects.create_superuser(
            email = 'admin@example.com',
            password = 'Django@123',
        )
        self.client.force_authenticate(user=superuser)

        url = detail_url(superuser.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_cannot_deactivate_superuser(self):
        """Superuser cannot deactivate superuser"""
        superuser1 = get_user_model().objects.create_superuser(
            email = 'admin@example.com',
            password = 'Django@123',
        )
        superuser2 = get_user_model().objects.create_superuser(
            email = 'staff@example.com',
            password = 'Django@123',
        )
        self.client.force_authenticate(user=superuser1)

        url = deactivate_user_url(superuser2.id)
        res = self.client.post(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        superuser2.refresh_from_db()
        self.assertTrue(superuser2.is_active)

    def test_superuser_can_deactivate_staff_user(self):
        """Superuser can deactivate staff user"""
        superuser = get_user_model().objects.create_superuser(
            email = 'admin@example.com',
            password = 'Django@123',
        )
        staff_user = create_user(
            email = 'staff@example.com',
            password = 'Django@123',
            is_staff = True
        )
        self.client.force_authenticate(user=superuser)

        url = deactivate_user_url(staff_user.id)
        res = self.client.post(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        staff_user.refresh_from_db()
        self.assertFalse(staff_user.is_active)
        self.assertIn("Deactivated", [group.name for group in staff_user.groups.all()])

    def test_staff_can_deactivate_normal_user(self):
        """Staff and superuser can deactivate normal user"""
        staff_user = create_user(
            email = 'staff@example.com',
            password = 'Django@123',
            is_staff = True
        )
        self.client.force_authenticate(user=staff_user)

        url = deactivate_user_url(self.user.id)
        res = self.client.post(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.assertIn("Deactivated", [group.name for group in self.user.groups.all()])

    def test_staff_cannot_deactivate_other_staff_user(self):
        """Staff user cannot deactivate other staff user"""
        staff_user1 = create_user(
            email = 'staff@example.com',
            password = 'Django@123',
            is_staff = True
        )
        staff_user2 = create_user(
            email = 'staff2@example.com',
            password = 'Django@123',
            is_staff = True
        )

        self.client.force_authenticate(user=staff_user1)

        url = deactivate_user_url(staff_user2.id)
        res = self.client.post(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        staff_user2.refresh_from_db()
        self.assertTrue(staff_user2.is_active)

    def test_staff_cannot_deactivate_themselves(self):
        """Staff user cannot deactivate themselves"""
        staff_user = create_user(
            email = 'staff@example.com',
            password = 'Django@123',
            is_staff = True
        )
        self.client.force_authenticate(user=staff_user)

        url = deactivate_user_url(staff_user.id)
        res = self.client.post(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        staff_user.refresh_from_db()
        self.assertTrue(staff_user.is_active)

    def test_normal_user_cannot_deactivate_other_user(self):
        """Normal user cannot deactivate other user"""
        user2 = get_user_model().objects.create_user(
            email="user1@example.com",
            password="Djanog@123",
        )

        url = deactivate_user_url(user2.id)
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        user2.refresh_from_db()
        self.assertTrue(user2.is_active)

    def test_normal_user_can_deactivate_themselves(self):
        """Normal user can deactivate themselves"""
        url = deactivate_user_url(self.user.id)
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_cannot_deactivate_inactive_user(self):
        """Cannot deactivate inactive user"""
        superuser = get_user_model().objects.create_superuser(
            email = 'admin@example.com',
            password = 'Django@123',
        )
        self.user.is_active = False
        self.user.save()

        self.client.force_authenticate(user=superuser)

        url = deactivate_user_url(self.user.id)
        res = self.client.post(url)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_superuser_can_activate_staff(self):
        superuser = get_user_model().objects.create_superuser(
            email = 'admin@example.com',
            password = 'Django@123',
        )
        staff_user = create_user(
            email = 'staff@example.com',
            password = 'Django@123',
            is_staff = True
        )
        staff_user.is_active = False
        staff_user.save()
        self.client.force_authenticate(user=superuser)

        url = reverse('user-activate-user', args=[staff_user.id])
        res = self.client.post(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        staff_user.refresh_from_db()
        self.assertTrue(staff_user.is_active)
        self.assertEqual(staff_user.groups.first().name, 'Default')

    def test_staff_can_activate_user(self):
        """Staff and superuser can activate user"""
        self.user.is_active = False
        self.user.save()
        staff_user = create_user(
            email = 'staff@example.com',
            password = 'Django@123',
            is_staff = True
        )

        self.client.force_authenticate(user=staff_user)
        url = reverse('user-activate-user', args=[self.user.id])
        res = self.client.post(url)

        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.is_active)
        self.assertEqual(self.user.groups.first().name, 'Default')

    def test_staff_cannot_activate_another_staff(self):
        staff_user1 = create_user(
            email = 'staff@example.com',
            password = 'Django@123',
            is_staff = True
        )
        staff_user2 = create_user(
            email = 'staff2@example.com',
            password = 'Django@123',
            is_staff = True
        )
        staff_user2.is_active = False
        staff_user2.save()

        self.client.force_authenticate(user=staff_user1)
        url = reverse('user-activate-user', args=[staff_user2.id])
        res = self.client.post(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        staff_user2.refresh_from_db()
        self.assertFalse(staff_user2.is_active)

    def test_staff_cannot_activate_themselves(self):
        staff_user = create_user(
            email = 'staff@example.com',
            password = 'Django@123',
            is_staff = True
        )
        staff_user.is_active = False
        staff_user.save()
        self.client.force_authenticate(user=staff_user)

        url = reverse('user-activate-user', args=[staff_user.id])
        res = self.client.post(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        staff_user.refresh_from_db()
        self.assertFalse(staff_user.is_active)

    def test_user_cannot_activate_themselves(self):
        self.user.is_active = False
        self.user.save()

        url = reverse('user-activate-user', args=[self.user.id])
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_user_cannot_activate_other_user(self):
        user2 = get_user_model().objects.create_user(
            email="user1@example.com",
            password="Djanog@123",
        )
        user2.is_active = False
        user2.save()

        url = reverse('user-activate-user', args=[user2.id])
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        user2.refresh_from_db()
        self.assertFalse(user2.is_active)

    def test_staff_cannot_activate_active_user(self):
        staff_user = create_user(
            email = 'staff@example.com',
            password = 'Django@123',
            is_staff = True
        )

        self.client.force_authenticate(user=staff_user)
        url = reverse('user-activate-user', args=[self.user.id])
        res = self.client.post(url)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)


class PrivateUserApiImageTests(APITestCase):
    """Test user profile image"""
    def setUp(self):
        "Environment Setup"
        # Create a 10x10 black image using Pillow
        black_image = Image.new("RGB", (10, 10), "black")

        # Save the image to BytesIO object
        image_bytes = io.BytesIO()
        black_image.save(image_bytes, format="JPEG")
        image_bytes.seek(0)

        # Create the image
        self.image = SimpleUploadedFile(
            name="test_image.jpg",
            content=image_bytes.read(),
            content_type="image/jpeg",
        )

        #Create the User
        self.user = get_user_model().objects.create_user(
            email="test@example.com",
            password="Django@123",
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        if os.path.exists(self.image_path):
            os.remove(self.image_path)
        self.user.delete()

    def test_update_user_profile_image(self):
        """Update user profile image"""
        url = image_upload_url(self.user.id)
        res = self.client.post(url, {'profile_img': self.image}, format='multipart')
        self.user.refresh_from_db()
        self.image_path = os.path.join(settings.MEDIA_ROOT, self.user.profile_img.name)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("profile_img", res.data)
        self.assertTrue(self.user.profile_img.name.endswith('test_image.jpg'))
        self.assertTrue(os.path.exists(self.user.profile_img.path))
