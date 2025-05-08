"""Test cases for Blog Model"""

from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from core_db.models import Blog, Category, Blog_Category

# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


def create_user(email, password):
    return get_user_model().objects.create_user(email=email, password=password)


class BlogModelTest(TestCase):
    """Test cases for Blog Model"""

    def setUp(self):
        self.user = create_user(email="test@example.com", password="Django@123")
        self.category = Category.objects.create(name="Test Category")

    def test_create_blog(self):
        """Test blog model"""
        blog = Blog.objects.create(
            title="Test Blog Title",
            content="c" * 101,
            author=self.user,
            overview="o" * 21,
        )
        self.assertEqual(blog.title, "Test Blog Title")
        self.assertEqual(blog.content, "c" * 101)
        self.assertEqual(blog.author, self.user)
        self.assertEqual(blog.overview, "o" * 21)
        self.assertEqual(blog.likes, 0)
        self.assertEqual(blog.cat_count, 0)
        self.assertEqual(blog.report_count, 0)
        self.assertAlmostEqual(
            blog.created_at, timezone.now(), delta=timezone.timedelta(seconds=5)
        )
        self.assertEqual(blog.status, "Draft")
        self.assertEqual(blog.visibility, False)
        self.assertEqual(blog.score, 0.0)
        self.assertEqual(blog.slug, "test-blog-title")
        self.assertEqual(str(blog), "Test Blog Title")

    def test_create_blog_without_title(self):
        """Test blog model without title"""
        with self.assertRaises(ValidationError):
            Blog.objects.create(
                content="c" * 101,
                author=self.user,
                overview="o" * 21,
            )

    def test_create_blog_without_author(self):
        """Test blog model without author"""
        with self.assertRaises(ValidationError):
            Blog.objects.create(
                title="Test Blog Title",
                content="c" * 101,
                overview="o" * 21,
            )

    def test_create_blog_without_overview(self):
        """Test blog model without overview"""
        with self.assertRaises(ValidationError):
            Blog.objects.create(
                title="Test Blog Title",
                content="c" * 101,
                author=self.user,
            )

    def test_create_blog_without_content(self):
        """Test blog model without content"""
        with self.assertRaises(ValidationError):
            Blog.objects.create(
                title="Test Blog Title",
                author=self.user,
                overview="o" * 21,
            )

    def test_invalid_blog_title_min_length(self):
        """Test blog title max length"""
        invalid_title = "t"
        with self.assertRaises(ValidationError) as context:
            Blog.objects.create(
                title=invalid_title,
                content="c" * 101,
                author=self.user,
                overview="o" * 21,
            )

        self.assertIn(
            "Title must be at least 10 characters long.",
            str(context.exception),
        )

    def test_invalid_blog_overview_min_length(self):
        """Test blog overview max length"""
        invalid_overview = "t"
        with self.assertRaises(ValidationError) as context:
            Blog.objects.create(
                title="Test Blog Title",
                content="c" * 101,
                author=self.user,
                overview=invalid_overview,
            )

        self.assertIn(
            "Overview must be at least 20 characters long.",
            str(context.exception),
        )

    def test_invalid_blog_content_min_length(self):
        """Test blog overview max length"""
        invalid_content = "t"
        with self.assertRaises(ValidationError) as context:
            Blog.objects.create(
                title="Test Blog Title",
                content=invalid_content,
                author=self.user,
                overview="o" * 21,
            )

        self.assertIn(
            "Context must be at least 100 characters long.",
            str(context.exception),
        )

    def test_invalid_blog_title_max_length(self):
        """Test blog title max length"""
        invalid_title = "t" * 101
        with self.assertRaises(ValidationError) as context:
            Blog.objects.create(
                title=invalid_title,
                content="c" * 101,
                author=self.user,
                overview="o" * 21,
            )

        self.assertIn(
            "Title cannot be longer than 100 characters.",
            str(context.exception),
        )

    def test_invalid_blog_overview_max_length(self):
        """Test blog overview max length"""
        invalid_overview = "t" * 151
        with self.assertRaises(ValidationError) as context:
            Blog.objects.create(
                title="Test Blog Title",
                content="c" * 101,
                author=self.user,
                overview=invalid_overview,
            )

        self.assertIn(
            "Overview cannot be longer than 150 characters.",
            str(context.exception),
        )

    def test_invalid_cat_count_max_count(self):
        """Test cat_count max count"""
        invalid_cat_count = 6
        with self.assertRaises(ValidationError) as context:
            Blog.objects.create(
                title="Test Blog Title",
                content="c" * 101,
                author=self.user,
                overview="o" * 21,
                cat_count=invalid_cat_count,
            )

        self.assertIn(
            "Cannot add more than 5 categories.",
            str(context.exception),
        )

    def test_update_exceeding_max_cat_count(self):
        """Test update exceeding max count"""
        blog = Blog.objects.create(
            title="Test Blog Title",
            content="c" * 101,
            author=self.user,
            overview="o" * 21,
            cat_count=5,
        )
        with self.assertRaises(ValidationError) as context:
            blog.cat_count = 6
            blog.save()

        self.assertIn(
            "Cannot add more than 5 categories.",
            str(context.exception),
        )

    def test_invalid_status_for_blog(self):
        """Test invalid status for blog"""
        with self.assertRaises(ValidationError):
            Blog.objects.create(
                title="Test Blog Title",
                content="c" * 101,
                author=self.user,
                overview="o" * 21,
                status="Invalid Status",
            )

    def test_create_blog_category(self):
        """Test create blog category"""
        blog = Blog.objects.create(
            title="Test Blog Title",
            content="c" * 101,
            author=self.user,
            overview="o" * 21,
        )
        blog_category = Blog_Category.objects.create(
            blog=blog,
            category=self.category,
        )
        self.assertEqual(str(blog_category), f"{blog.title} - {self.category.name}")
        self.assertEqual(blog.cat_count, 1)

    def test_duplicate_blog_category(self):
        """Test duplicate blog category"""
        blog = Blog.objects.create(
            title="Test Blog Title",
            content="c" * 101,
            author=self.user,
            overview="o" * 21,
        )
        Blog_Category.objects.create(
            blog=blog,
            category=self.category,
        )
        with self.assertRaises(ValidationError):
            Blog_Category.objects.create(
                blog=blog,
                category=self.category,
            )

    def test_invalid_cat_count_blog_category(self):
        """Test blog cat_count exceeds while creating blog category"""
        blog = Blog.objects.create(
            title="Test Blog Title",
            content="c" * 101,
            author=self.user,
            overview="o" * 21,
            cat_count=5,
        )

        with self.assertRaises(ValidationError) as context:
            Blog_Category.objects.create(
                blog=blog,
                category=self.category,
            )

        self.assertIn(
            "Cannot add more than 5 categories.",
            str(context.exception),
        )
