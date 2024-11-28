"""Test Cases for blog"""
import os, io
from django.test import TestCase
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from blog_api.models import Blog, Category
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from blog_api.serializers import BlogSerializer, BlogImageSerializer


class BlogModelTests(TestCase):
    """Test Cases for Blog Model"""

    def setUp(self):
        self.user = get_user_model().objects.create(
            email="test@example.com",
            password="Django@123",
        )

        self.category = Category.objects.create(
            name="cat1"
        )

        self.b_title = "Valid Title"
        self.b_content = "Valid content created"
        self.blog = Blog.objects.create(
            title=self.b_title,
            content=self.b_content,
            author=self.user
        )

    def test_creating_blog_with_valid_data(self):
        """Creating a blog with valid data"""
        self.assertEqual(self.blog.title, self.b_title)
        self.assertEqual(self.blog.content, self.b_content)
        self.assertEqual(self.blog.author, self.user)

    def test_adding_category_to_blog(self):
        """Category addition to blog"""
        self.blog.categories.add(self.category)
        self.assertIn(self.category, self.blog.categories.all())

    def test_creating_blog_without_title(self):
        """Test Creating a blog without title"""
        with self.assertRaises(ValidationError):
            blog1 = Blog.objects.create(
                content=self.b_content,
                author=self.user
            )

    def test_creating_blog_without_content(self):
        """Test Creating a blog without content"""
        with self.assertRaises(ValidationError):
            blog1 = Blog.objects.create(
                title = self.b_title,
                author=self.user
            )

    def test_creating_blog_without_author(self):
        """Test Creating a blog without an author"""
        with self.assertRaises(ValidationError):
            blog1 = Blog.objects.create(
                title = self.b_title,
                content=self.b_content,
            )

    def test_creating_blog_slug(self):
        """Blog slug should be created automatically"""
        self.assertEqual(self.blog.slug, "valid-title")

    def test_updating_blog_slug_with_title_update(self):
        """Blog slug should be updated when title is updated"""
        self.blog.title = "Updated Title"
        self.blog.save()
        self.assertEqual(self.blog.slug, "updated-title")

class BlogModelImageTests(TestCase):
    """Test Cases for Blog Model with Image"""
    def setUp(self):
        black_image = Image.new("RGB", (10, 10), "black")

        image_bytes=io.BytesIO()
        black_image.save(image_bytes, format="JPEG")
        image_bytes.seek(0)

        self.image = SimpleUploadedFile(
            name="test_image.jpg",
            content=image_bytes.read(),
            content_type="image/jpeg"
        )

        self.user = get_user_model().objects.create_user(
            email="test@example.com",
            password="Django@123"
        )

        self.blog = Blog.objects.create(
            title="Valid Title",
            content="Valid Content Created",
            author=self.user
        )

    def tearDown(self):
        if os.path.exists(self.image_path):
            os.remove(self.image_path)
        self.blog.delete()

    def test_blog_with_image(self):
        """Test creating a blog with an image"""
        self.blog.blog_image = self.image
        self.blog.save()
        self.image_path = os.path.join(settings.MEDIA_ROOT, self.blog.blog_image.name)

        self.assertTrue(self.blog.blog_image)
        self.assertEqual(self.blog.blog_image.name, "blog_images/test_image.jpg")
        self.assertTrue(os.path.exists(self.image_path))


BLOGS_URL = reverse('blog-list')

def detail_url(blog_id):
    """BLOG detail URL"""
    return reverse('blog-detail', args=[blog_id])

def image_upload_url(blog_id):
    """Blog image upload URL"""
    return reverse('blog-upload-image', args=[blog_id])

def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)

def create_blog(**params):
    """Create and return a new blog"""
    return Blog.objects.create(**params)

class PublicBlogApiTests(APITestCase):
    """Public Blog API Tests"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(BLOGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateBlogApiTests(APITestCase):
    """Private Blog API Tests"""
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email = "test@example.com",
            password = "Django@123",
        )
        self.category = Category.objects.create(
            name = "cat1",
        )
        self.blog_params = {
            'author': self.user,
            'title': 'Test Blog',
            'content': 'Test Content',
        }
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


    def test_create_and_retrieve_blogs(self):
        """Test creating and retrieving blogs"""
        self.blog_params['author'] = self.user.id
        res_created = self.client.post(BLOGS_URL, self.blog_params)
        self.assertEqual(res_created.status_code, status.HTTP_201_CREATED)

        res = self.client.get(BLOGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        blogs = Blog.objects.all()
        serilaizer = BlogSerializer(blogs, many=True, context={'request': res.wsgi_request})
        self.assertEqual(res.data, serilaizer.data)

    def test_create_blog_with_invalid_data(self):
        """Test creating a blog with invalid data"""
        res = self.client.post(BLOGS_URL, {
            'title': '',
        })
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_blog_with_new_categories(self):
        """Test creating a blog with categories"""
        self.blog_params['author'] = self.user.id
        self.blog_params['categories'] = [
            {'name': 'cat2'},
            {'name': 'cat3'},
        ]
        res = self.client.post(BLOGS_URL, self.blog_params, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(BLOGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        blog = Blog.objects.get(title=self.blog_params['title'])
        cat = Category.objects.all()
        serilaizer = BlogSerializer(blog, context={'request': res.wsgi_request})
        self.assertEqual(res.data[0], serilaizer.data)
        self.assertEqual(blog.categories.count(), 2)
        self.assertEqual(cat.count(), 3)
        self.assertNotIn(self.category, blog.categories.all())

    def test_create_blog_with_existing_categories(self):
        """Test creating a blog with categories"""
        self.blog_params['author'] = self.user.id
        self.blog_params['categories'] = [{'name': self.category.name},]
        res = self.client.post(BLOGS_URL, self.blog_params, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(BLOGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        blog = Blog.objects.filter(title=self.blog_params['title'])
        serilaizer = BlogSerializer(blog, many=True, context={'request': res.wsgi_request})
        self.assertEqual(res.data, serilaizer.data)
        self.assertEqual(res.data[0]['categories'][0]['name'], self.category.name)

    def test_update_own_with_categories_blog(self):
        """Test updating a blog"""
        blog = create_blog(**self.blog_params)
        blog.categories.add(self.category)
        payload = {
            'title': 'Updated Title',
            'content': 'Updated Content',
            'categories': [{'name': 'cat2'}],
        }

        url = detail_url(blog.id)
        res = self.client.patch(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        blog.refresh_from_db()
        self.assertEqual(blog.title, payload['title'])
        self.assertEqual(blog.content, payload['content'])
        self.assertEqual(blog.categories.count(), 1)

    def test_update_another_user_blog_as_staff(self):
        """Test updating another user's blog"""
        user2 = create_user(
            email='user2@example.com',
            password='Django@123',
            is_staff=True
        )
        self.blog_params['author'] = user2
        blog = create_blog(**self.blog_params)
        payload = {
            'title': 'Updated Title',
            'content': 'Updated Content',
        }

        url = detail_url(blog.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_another_user_blog_as_superuser(self):
        """Test updating another user's blog"""
        superuser = get_user_model().objects.create_superuser(
            email='superuser@example.com',
            password='Django@123',
        )
        blog = create_blog(**self.blog_params)
        payload = {
            'title': 'Updated Title',
            'content': 'Updated Content',
        }

        self.client.force_authenticate(user=superuser)
        url = detail_url(blog.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_own_blog(self):
        """Test deleting a blog"""
        blog = create_blog(**self.blog_params)
        url = detail_url(blog.id)

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        exists = Blog.objects.filter(id=blog.id).exists()
        self.assertFalse(exists)

    def test_delete_another_user_blog(self):
        user2 = create_user(
            email='user2@example.com',
            password='Django@123',
        )
        self.blog_params['author'] = user2
        blog = create_blog(**self.blog_params)
        url = detail_url(blog.id)

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_another_user_blog_as_staff(self):
        """Test deleting another user's blog"""
        staff = create_user(
            email='user2@example.com',
            password='Django@123',
            is_staff=True
        )
        self.client.force_authenticate(user=staff)
        blog = create_blog(**self.blog_params)
        url = detail_url(blog.id)

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_another_user_blog_as_superuser(self):
        """Test deleting another user's blog"""
        superuser = get_user_model().objects.create_superuser(
            email='superuser@example.com',
            password='Django@123',
        )
        self.client.force_authenticate(user=superuser)
        blog = create_blog(**self.blog_params)
        url = detail_url(blog.id)

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


class PrivateBlogApiImageTests(APITestCase):
    """Test uploading images to a blog"""
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

        # Create the User
        self.user = get_user_model().objects.create_user(
            email="test@example.com",
            password="Django@123",
        )
        # Create the Blog parameters
        self.blog_params = {
            'author': self.user,
            'title': 'Test Blog',
            'content': 'Test Content',
        }
        # Create the Blog
        self.blog = create_blog(**self.blog_params)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        if os.path.exists(self.image_path):
            os.remove(self.image_path)
        self.user.delete()

    def test_update_user_profile_image(self):
        """Update user profile image"""
        url = image_upload_url(self.blog.id)
        res = self.client.post(url, {'blog_image': self.image}, format='multipart')
        self.blog.refresh_from_db()
        self.image_path = os.path.join(settings.MEDIA_ROOT, self.blog.blog_image.name)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("blog_image", res.data)
        self.assertTrue(self.blog.blog_image.name.endswith('test_image.jpg'))
        self.assertTrue(os.path.exists(self.blog.blog_image.path))