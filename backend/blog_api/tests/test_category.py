"""Test Cases for Category"""
from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from blog_api.models import Category, Blog
from blog_api.serializers import CategorySerializer


class CategoryModelTests(TestCase):
    """Test cases for the Category Model"""

    def test_category_creation(self):
        """Creating a Category"""
        cat_name = "cat1"
        category = Category.objects.create(
            name=cat_name
        )

        self.assertEqual(category.name, cat_name)

    def test_blank_and_null_category_creation(self):
        """Raising error for blank and null category"""
        cat_name = ["", None]
        for i in range(len(cat_name)):
            with self.assertRaises(ValidationError):
                category1 = Category.objects.create(
                    name=cat_name[i]
                )

    def test_creating_user_slug(self):
        """Test creating a user with a slug"""
        slug = 'cat-1'
        cat = Category.objects.create(
            name='cat 1',
        )
        self.assertEqual(cat.slug, slug)

    def test_updating_blog_slug_with_title_update(self):
        """Blog slug should be updated when title is updated"""
        cat = Category.objects.create(
            name='cat 1',
        )
        cat.name = "cat 2"
        cat.save()
        self.assertEqual(cat.slug, "cat-2")

CATEGORIES_URL = reverse('category-list')

def detail_url(category_id):
    """Create and return a category detail URL"""
    return reverse('category-detail', args=[category_id])

def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)

class PublicCategoryApiTests(APITestCase):
    """Public tests for Category API"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving categories"""

        res = self.client.get(CATEGORIES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateCategoryApiTests(APITestCase):
    """Private tests for Category API"""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='Django@123',
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_and_retrieve_categories(self):

        payload = {
            'name': 'cat1',
        }
        res_create = self.client.post(CATEGORIES_URL, payload)
        self.assertEqual(res_create.status_code, status.HTTP_201_CREATED)

        res = self.client.get(CATEGORIES_URL)
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_unique_category_only(self):

        payload = {
            'name': 'cat1',
        }
        res = self.client.post(CATEGORIES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res_duplicate = self.client.post(CATEGORIES_URL, payload)
        self.assertEqual(res_duplicate.status_code, status.HTTP_201_CREATED)

        categories = Category.objects.filter(name=payload['name'])
        self.assertEqual(categories.count(), 1)

    def test_update_category(self):

        cat = Category.objects.create(name='cat1')
        payload = {
            'name': 'cat2',
        }
        url = detail_url(cat.id)

        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        cat.refresh_from_db()
        self.assertEqual(cat.name, payload['name'])

    def test_delete_category(self):

        cat = Category.objects.create(name='cat1')
        url = detail_url(cat.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        exists = Category.objects.filter(
            name = 'cat1',
        ).exists()
        self.assertFalse(exists)

    def test_categories_assigned_to_blog_exists(self):

        cat1 = Category.objects.create(name='cat1')

        blog = Blog.objects.create(
            title = 'blog1',
            content = 'blog1',
            author = self.user,
        )

        blog.categories.add(cat1)

        res = self.client.get(CATEGORIES_URL)
        serilaizer1 = CategorySerializer(cat1)
        self.assertIn(serilaizer1.data, res.data)
