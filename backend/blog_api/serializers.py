"""Serializers for blog api"""

from rest_framework import serializers
from core_db.models import Category, User_Category


class CategorySerializer(serializers.ModelSerializer):
    """Category Serializer"""

    class Meta:
        model = Category
        fields = ["id", "name"]


class UserCategorySerializer(serializers.ModelSerializer):
    """User Category Serializer"""

    class Meta:
        model = User_Category
        fields = ["id", "user", "category"]
