# pylint: skip-file

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from core_db.models import Category, User_Category

# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


CATEGORY_URL = reverse("category")
USER_CATEGORY_URL = reverse("user-category")
USER_CATGEORY_RETRIEVE_URL = reverse("user-category-retreive")


def category_detail_url(cat_id):
    """Create and return a user detail URL"""
    return reverse("category-detail", args=[cat_id])


def user_category_retrieve_url(user_id):
    """Create and return a user detail URL"""
    return reverse("user-category-retrieve", args=[user_id])


def user_category_delete_url(user_cat_id):
    """Create and return a user detail URL"""
    return reverse("user-category", args=[user_cat_id])


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicCategoryTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Sample Category")

    def test_list_all_categories(self):
        """List all the categories"""
        res = self.client.get(CATEGORY_URL)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], "Sample Category")

    def test_retrieve_category(self):
        """Retrieve a single category"""
        res = self.client.get(category_detail_url(self.category.id))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["name"], "Sample Category")

    def test_retrieve_nonexistent_category(self):
        """Retrieve a non-existent category"""
        res = self.client.get(category_detail_url(999))
        self.assertEqual(res.status_code, 404)

    def test_create_category(self):
        """Create a new category"""
        payload = {"name": "Test Category"}
        res = self.client.post(CATEGORY_URL, payload)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(Category.objects.count(), 1)

    def test_update_category(self):
        """Update a category"""
        payload = {"name": "Updated Category"}
        res = self.client.put(category_detail_url(self.category.id), payload)
        self.assertEqual(res.status_code, 401)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Sample Category")

    def test_partial_update_category(self):
        """Partial Update a category"""
        payload = {"name": "Partially Updated Category"}
        res = self.client.patch(category_detail_url(self.category.id), payload)
        self.assertEqual(res.status_code, 401)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Sample Category")

    def test_delete_category(self):
        """Delete a category"""
        res = self.client.delete(category_detail_url(self.category.id))
        self.assertEqual(res.status_code, 401)
        self.assertTrue(Category.objects.filter(id=self.category.id).exists())


class PrivateCategoryTest(APITestCase):
    def setUp(self):
        self.superuser = get_user_model().objects.create_superuser(
            email="superuser@example.com",
            password="SuperUser@123",
        )
        self.staff = create_user(
            email="staff@example.com",
            password="Django@123",
            is_staff=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(self.superuser)
        self.category = Category.objects.create(name="Sample Category")

    def test_superuser_can_create_category(self):
        """Create a new category as superuser"""
        payload = {"name": "Test Category"}
        res = self.client.post(CATEGORY_URL, payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data["name"], "Test Category")
        self.assertEqual(Category.objects.count(), 2)
        category = Category.objects.get(id=res.data["id"])
        self.assertEqual(category.name, "Test Category")

    def test_staff_cannot_create_category(self):
        """Cannot create a new category as staff"""
        self.client.force_authenticate(self.staff)
        payload = {"name": "Test Category"}
        res = self.client.post(CATEGORY_URL, payload)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(Category.objects.count(), 1)

    def test_create_category_invalid_payload(self):
        """Cannot create a new category with invalid payload"""
        payload = {"name": ""}
        res = self.client.post(CATEGORY_URL, payload)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(Category.objects.count(), 1)

    def test_update_category(self):
        """Update a category (NOT ALLOWED)"""
        payload = {"name": "Updated Category"}
        res = self.client.put(category_detail_url(self.category.id), payload)
        self.assertEqual(res.status_code, 405)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Sample Category")

    def test_partial_update_category(self):
        """Partial Update a category (NOT ALLOWED)"""
        payload = {"name": "Partially Updated Category"}
        res = self.client.patch(category_detail_url(self.category.id), payload)
        self.assertEqual(res.status_code, 405)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Sample Category")

    def test_superuser_can_delete_category(self):
        """Delete a category as superuser"""
        res = self.client.delete(category_detail_url(self.category.id))
        self.assertEqual(res.status_code, 204)
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())

    def test_staff_cannot_delete_category(self):
        """Cannot delete a category as staff"""
        self.client.force_authenticate(self.staff)
        res = self.client.delete(category_detail_url(self.category.id))
        self.assertEqual(res.status_code, 403)
        self.assertTrue(Category.objects.filter(id=self.category.id).exists())

    def test_delete_nonexistent_category(self):
        """Cannot delete a non-existent category"""
        res = self.client.delete(category_detail_url(999))
        self.assertEqual(res.status_code, 404)


class PublicUserCategoryTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email="test@example.com",
            password="Django@123",
        )
        self.category = Category.objects.create(name="Sample Category")
        self.user_category = User_Category.objects.create(
            user=self.user, category=self.category
        )

    def test_list_all_user_category_url(self):
        """List all the user categories"""
        res = self.client.get(USER_CATEGORY_URL)
        self.assertEqual(res.status_code, 401)

    def test_list_all_user_category_retrieve_url(self):
        """List all the user categories"""
        res = self.client.get(USER_CATGEORY_RETRIEVE_URL)
        self.assertEqual(res.status_code, 401)

    def test_retrieve_user_category_retrieve_url(self):
        """Retrieve a single user category"""
        res = self.client.get(user_category_retrieve_url(self.user.id))
        self.assertEqual(res.status_code, 401)

    def test_retrieve_user_category_delete_url(self):
        """Retrieve a single user category"""
        res = self.client.get(user_category_delete_url(self.user_category.id))
        self.assertEqual(res.status_code, 401)

    def test_create_user_category_url(self):
        """Cannot create a new user category"""
        payload = {"user": self.user.id, "category": self.category.id}
        res = self.client.post(USER_CATEGORY_URL, payload)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(User_Category.objects.count(), 1)

    def test_create_user_category_retrieve_url(self):
        """Cannot create a new user category"""
        payload = {"user": self.user.id, "category": self.category.id}
        res = self.client.post(USER_CATGEORY_RETRIEVE_URL, payload)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(User_Category.objects.count(), 1)

    def test_update_user_category_retrieve_url(self):
        """Cannot update a user category"""
        payload = {"user": self.user.id, "category": self.category.id}
        res = self.client.put(user_category_retrieve_url(self.user.id), payload)
        self.assertEqual(res.status_code, 401)
        self.user_category.refresh_from_db()
        self.assertEqual(self.user_category.user, self.user)

    def test_update_user_category_delete_url(self):
        """Cannot update a user category"""
        payload = {"user": self.user.id, "category": self.category.id}
        res = self.client.put(user_category_delete_url(self.user_category.id), payload)
        self.assertEqual(res.status_code, 401)
        self.user_category.refresh_from_db()
        self.assertEqual(self.user_category.user, self.user)

    def test_partial_update_user_category_retrieve_url(self):
        """Cannot partial update a user category"""
        payload = {"user": self.user.id, "category": self.category.id}
        res = self.client.patch(
            user_category_retrieve_url(self.user_category.id), payload
        )
        self.assertEqual(res.status_code, 401)
        self.user_category.refresh_from_db()
        self.assertEqual(self.user_category.user, self.user)

    def test_partial_update_user_category_delete_url(self):
        """Cannot partial update a user category"""
        payload = {"user": self.user.id, "category": self.category.id}
        res = self.client.patch(
            user_category_delete_url(self.user_category.id), payload
        )
        self.assertEqual(res.status_code, 401)
        self.user_category.refresh_from_db()
        self.assertEqual(self.user_category.user, self.user)

    def test_delete_user_category_retrieve_url(self):
        """Cannot delete a user category"""
        res = self.client.delete(user_category_retrieve_url(self.user.id))
        self.assertEqual(res.status_code, 401)
        self.assertTrue(User_Category.objects.filter(id=self.user.id).exists())

    def test_delete_user_category_delete_url(self):
        """Cannot delete a user category"""
        res = self.client.delete(user_category_delete_url(self.user_category.id))
        self.assertEqual(res.status_code, 401)
        self.assertTrue(User_Category.objects.filter(id=self.user_category.id).exists())


# class PrivateUserCategoryTest(APITestCase):
#     def setUp(self):
#         self.superuser = get_user_model().objects.create_superuser(
#             email="superuser@example.com",
#             password="SuperUser@123",
#         )
#         self.staff = create_user(
#             email="staff@example.com",
#             password="Django@123",
#             is_staff=True,
#         )
#         self.user = create_user(
#             email="test@example.com",
#             password="Django@123",
#         )
#         self.other_user = create_user(
#             email="other@example.com",
#             password="Django@123",
#         )
#         self.client = APIClient()
#         self.client.force_authenticate(self.user)
#         self.category = Category.objects.create(name="Sample Category")
#         self.user_category = User_Category.objects.create(
#             user=self.user, category=self.category
#         )
#         self.other_user_category = User_Category.objects.create(
#             user=self.other_user, category=self.category
#         )

#     def test_list_user_category(self):
#         """List only the authenticated user's categories"""
#         res = self.client.get(USER_CATEGORY_URL)
#         self.assertEqual(res.status_code, 405)

#     def test_retrieve_user_category(self):
#         """Retrieve a single user category for the authenticated user"""
#         res = self.client.get(user_category_detail_url(self.user.id))
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res.data["id"], self.user_category.id)
#         self.assertEqual(res.data["user"], self.user.id)
#         self.assertEqual(res.data["category"], self.category.id)

#     def test_retrieve_other_user_category_forbidden(self):
#         """Cannot retrieve another user's category"""
#         res = self.client.get(user_category_detail_url(self.other_user.id))
#         self.assertEqual(res.status_code, 403)

#     def test_create_user_category(self):
#         """Create a new user category for the authenticated user"""
#         new_category = Category.objects.create(name="New Category")
#         payload = {"user": self.user, "category": new_category}
#         res = self.client.post(USER_CATEGORY_URL, payload)
#         self.assertEqual(res.status_code, 201)
#         self.assertEqual(User_Category.objects.count(), 3)
#         user_category = User_Category.objects.get(user=self.user, category=new_category)
#         self.assertEqual(user_category.user, self.user)
#         self.assertEqual(user_category.category, new_category)

#     def test_delete_user_category(self):
#         """User can delete their own category"""
#         res = self.client.delete(user_category_detail_url(self.user_category.id))
#         self.assertEqual(res.status_code, 204)
#         self.assertFalse(
#             User_Category.objects.filter(id=self.user_category.id).exists()
#         )

#     def test_delete_other_user_category_forbidden(self):
#         """Cannot delete another user's category"""
#         res = self.client.delete(user_category_detail_url(self.other_user_category.id))
#         self.assertEqual(res.status_code, 403)
#         self.assertTrue(
#             User_Category.objects.filter(id=self.other_user_category.id).exists()
#         )

#     def test_update_user_category_not_allowed(self):
#         """Cannot update a user category (PUT)"""
#         payload = {"user": self.user.id, "category": self.category.id}
#         res = self.client.put(user_category_detail_url(self.user_category.id), payload)
#         self.assertEqual(res.status_code, 405)

#     def test_partial_update_user_category_not_allowed(self):
#         """Cannot partially update a user category (PATCH)"""
#         payload = {"user": self.user.id}
#         res = self.client.patch(
#             user_category_detail_url(self.user_category.id), payload
#         )
#         self.assertEqual(res.status_code, 405)

#     def test_superuser_cannot_access_other_user_category(self):
#         """Superuser cannot access another user's category"""
#         self.client.force_authenticate(self.superuser)
#         res = self.client.get(user_category_detail_url(self.user.id))
#         self.assertEqual(res.status_code, 403)

#     def test_superuser_cannot_delete_other_user_category(self):
#         """Superuser cannot delete another user's category"""
#         self.client.force_authenticate(self.superuser)
#         res = self.client.delete(user_category_detail_url(self.user_category.id))
#         self.assertEqual(res.status_code, 403)
#         self.assertTrue(User_Category.objects.filter(id=self.user_category.id).exists())

#     def test_staff_cannot_access_other_user_category(self):
#         """Staff cannot access another user's category"""
#         self.client.force_authenticate(self.staff)
#         res = self.client.get(user_category_detail_url(self.user_category.id))
#         self.assertEqual(res.status_code, 403)

#     def test_staff_cannot_delete_other_user_category(self):
#         """Staff cannot delete another user's category"""
#         self.client.force_authenticate(self.staff)
#         res = self.client.delete(user_category_detail_url(self.user_category.id))
#         self.assertEqual(res.status_code, 403)
#         self.assertTrue(User_Category.objects.filter(id=self.user_category.id).exists())
