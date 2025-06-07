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


class BlogCategorySerializer(serializers.ModelSerializer):
    """Blog Category Serializer"""

    class Meta:
        model = Blog_Category
        fields = ("id", "blog", "category")
