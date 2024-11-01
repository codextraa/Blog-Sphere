"""Test Cases for the User model."""
import os
from django.conf import settings
from django.test import TestCase
from blog_api.models import User, Category, Blog
from django.core.files.uploadedfile import SimpleUploadedFile
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

        self.test_image_path = os.path.join(settings.MEDIA_ROOT, 'profile_images')
        if not os.path.exists(self.test_image_path):
            os.makedirs(self.test_image_path)

    def tearDown(self):
        """Clean up after each test."""
        # Remove test images if they exist
        for filename in os.listdir(self.test_image_path):
            file_path = os.path.join(self.test_image_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

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

    def test_create_user_with_profile_image(self):
        """Test that a User can be created with a profile image."""
        mock_image = SimpleUploadedFile(
            name='test_profile_image.jpg',
            content=b'file_content',
            content_type='image/jpeg'
        )

        self.user.profile_img = mock_image
        self.user.save()

        # Verify that the user was created and the image is stored correctly
        self.assertEqual(self.user.profile_img.name, 'profile_images/test_profile_image.jpg')
        self.assertTrue(os.path.exists(os.path.join(settings.MEDIA_ROOT, self.user.profile_img.name)))

class CategoryModelTest(TestCase):
    """Test the Category model."""

    def setUp(self):
        """Create a Category instance for testing."""
        self.category = Category.objects.create(name='Test Category')

    def test_category_creation(self):
        """Test that the Category is created successfully."""
        self.assertEqual(self.category.name, 'Test Category')

    def test_str_method(self):
        """Test the string representation of the Category."""
        self.assertEqual(str(self.category), 'Test Category')

    def test_category_name_max_length(self):
        """Test that the name field has the correct max length."""
        max_length = self.category._meta.get_field('name').max_length
        self.assertEqual(max_length, 255)

    def test_category_name_can_be_updated(self):
        """Test that the Category name can be updated."""
        self.category.name = 'Updated Category'
        self.category.save()
        self.assertEqual(Category.objects.get(id=self.category.id).name, 'Updated Category')

    def test_category_creation_without_name(self):
        """Test that creating a Category without a name raises an error."""
        with self.assertRaises(ValidationError):
            Category.objects.create(name='')


class BlogModelTest(TestCase):

    def setUp(self):
        """Set up a User and Category for testing Blog creation."""
        self.user = User.objects.create_user(
            email='author@example.com',
            username='author',
            password='Password123!',
            first_name='First',
            last_name='Last'
        )
        self.category = Category.objects.create(name='Test Category')

        self.test_image_path = os.path.join(settings.MEDIA_ROOT, 'blog_images')
        if not os.path.exists(self.test_image_path):
            os.makedirs(self.test_image_path)

    def tearDown(self):
        """Clean up the test image directory."""
        for filename in os.listdir(self.test_image_path):
            file_path = os.path.join(self.test_image_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    def test_create_blog_with_valid_data(self):
        """Test that a Blog can be created with valid data."""
        blog = Blog.objects.create(
            title='Valid Blog Title',
            content='This is the content of the blog.',
            author=self.user
        )
        self.assertEqual(blog.title, 'Valid Blog Title')
        self.assertEqual(blog.content, 'This is the content of the blog.')
        self.assertEqual(blog.author, self.user)

    def test_create_blog_without_title(self):
        """Test that creating a Blog without a title raises a ValidationError."""
        with self.assertRaises(ValidationError):
            Blog.objects.create(
                title='',
                content='This is the content of the blog.',
                author=self.user
            )

    def test_create_blog_without_content(self):
        """Test that creating a Blog without content is not allowed."""
        with self.assertRaises(ValidationError):
            Blog.objects.create(
                title='Blog Without Content',
                content='',  # Empty content
                author=self.user
            )

    def test_create_blog_without_author(self):
        """Test that creating a Blog without an author raises an IntegrityError."""
        with self.assertRaises(Exception):  # Catch IntegrityError
            Blog.objects.create(
                title='Blog Without Author',
                content='This blog has no author.'
            )

    def test_create_blog_with_image(self):
        """Test that a Blog can be created with an image."""
        # This requires a mock or test image file

        mock_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'file_content',
            content_type='image/jpeg'
        )

        blog = Blog.objects.create(
            title='Blog with Image',
            content='This blog has an image.',
            image=mock_image,
            author=self.user
        )
        self.assertEqual(blog.image.name, 'blog_images/test_image.jpg')  # Ensure image is saved correctly

    def test_create_blog_with_categories(self):
        """Test that a Blog can be created with categories."""
        blog = Blog.objects.create(
            title='Blog with Categories',
            content='This blog is categorized.',
            author=self.user
        )
        blog.category.add(self.category)

        self.assertIn(self.category, blog.category.all())  # Check if category is associated with the blog

    def test_update_blog(self):
        """Test that a Blog can be updated."""
        blog = Blog.objects.create(
            title='Initial Title',
            content='Initial content.',
            author=self.user
        )
        blog.title = 'Updated Title'
        blog.save()

        self.assertEqual(blog.title, 'Updated Title')

    def test_delete_blog(self):
        """Test that a Blog can be deleted."""
        blog = Blog.objects.create(
            title='Blog to Delete',
            content='Content of the blog to be deleted.',
            author=self.user
        )
        blog_id = blog.id
        blog.delete()

        # Ensure the blog no longer exists
        with self.assertRaises(Blog.DoesNotExist):
            Blog.objects.get(id=blog_id)