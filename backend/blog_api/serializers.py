"""Serializers for blog api"""

from rest_framework import serializers
from core_db.models import Category, User_Category, Blog, Blog_Category


class CategorySerializer(serializers.ModelSerializer):
    """Category Serializer"""

    class Meta:
        model = Category
        fields = ("id", "name")


class UserCategorySerializer(serializers.ModelSerializer):
    """User Category Serializer"""

    class Meta:
        model = User_Category
        fields = ("id", "user", "category")


class BlogSerializer(serializers.ModelSerializer):
    """Blog Serializer"""

    author_email = serializers.CharField(source="author.email")
    author_username = serializers.CharField(source="author.username")
    author_first_name = serializers.CharField(source="author.first_name")
    author_last_name = serializers.CharField(source="author.last_name")
    category_names = serializers.SerializerMethodField()

    class Meta:  # pylint: disable=R0801
        model = Blog
        fields = (
            "id",
            "title",
            "content",
            "overview",
            "author",
            "likes",
            "cat_count",
            "report_count",
            "status",
            "visibility",
            "created_at",
            "score",
            "slug",
        )

    def get_category_names(self, obj):
        return [bc.category.name for bc in obj.categories.all()]


class BlogCategorySerializer(serializers.ModelSerializer):
    """Blog Category Serializer"""

    class Meta:
        model = Blog_Category
        fields = ("id", "blog", "category")
