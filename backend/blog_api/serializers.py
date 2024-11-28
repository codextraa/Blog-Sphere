"""Serializers For Blog API."""
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Category, Blog

class UserSerializer(serializers.ModelSerializer):
    """User Serializer."""

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'password', 'username', 'first_name', 'last_name',
                  'phone_number', 'profile_img', 'slug', 'is_active', 'is_staff']
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        profile_img = validated_data.pop('profile_img', None)

        if not profile_img:
            """Set default profile image if not provided"""
            default_image_path = 'profile_images/default_profile.jpg'
            validated_data['profile_img'] = default_image_path

        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return an existing user"""
        password = validated_data.pop("password", None)
        instance = super().update(instance, validated_data)

        if password:
            instance.set_password(password)
            instance.save()

        return instance

class UserImageSerializer(serializers.ModelSerializer):
    """User Serializer for Images"""
    class Meta:
        model = get_user_model()
        fields = ['id', 'profile_img']
        read_only_fields = ['id']

    def validate_profile_img(self, value):
        """Validate profile image"""
        max_size = 5 * 1024 * 1024 # 5MB
        valid_file_types = ['image/jpeg', 'image/png', 'image/gif'] # valid image types

        if value.size > max_size:
            raise serializers.ValidationError("Image size should be less than 5MB")

        if value.content_type not in valid_file_types:
            raise serializers.ValidationError("Invalid file type. Only JPEG, PNG, and GIF images are allowed.")

        return value

class CategorySerializer(serializers.ModelSerializer):
    """Category Serializer."""
    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a category or if exists return it."""
        category_name = validated_data.get('name')
        category, _ = Category.objects.get_or_create(name=category_name)
        return category


class BlogSerializer(serializers.ModelSerializer):
    """Blog Serializer."""
    categories = CategorySerializer(many=True, required=False)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'blog_image', 'created_at',
                  'slug', 'updated_at', 'author', 'categories']
        read_only_fields = ['id']

    # many to many fields handling
    def _get_or_create_categories(self, cats, blog): # Private method
        """Handle getting or creating categories as needed."""
        # auth_user = self.context['request'].user # applicable is user is foreign key
        for cat in cats:
            cat_obj, _ = Category.objects.get_or_create(
                # user = auth_user
                **cat,
            )
            blog.categories.add(cat_obj)

    def create(self, validated_data):
        """Create a blog"""
        cats = validated_data.pop('categories', []) # if category not found default to empty
        blog_image = validated_data.pop('blog_image', [])
        blog = Blog.objects.create(**validated_data)
        self._get_or_create_categories(cats, blog)

        if not blog_image:
            default_path = 'blog_images/default_image.jpg'
            blog.blog_image = default_path
        else:
            image_serializer = BlogImageSerializer(
                blog,
                data={'blog_image': blog_image},
                partial=True
            )
            image_serializer.is_valid(raise_exception=True)
            image_serializer.save()

        blog.save()
        return blog

    def update(self, instance, validated_data):
        """Update a blog"""
        cats = validated_data.pop('categories', [])
        blog_image = validated_data.pop('blog_image', [])
        instance = super().update(instance, validated_data)

        if cats is not None:
            instance.categories.clear()
            self._get_or_create_categories(cats, instance)

        if blog_image:
            image_serializer = BlogImageSerializer(
                instance,
                data = {'blog_image': blog_image},
                partial=True
            )
            image_serializer.is_valid(raise_exception=True)
            image_serializer.save()

        instance.save()
        return instance

class BlogImageSerializer(serializers.ModelSerializer):
    """Blog Image Serializer"""
    class Meta:
        model = Blog
        fields = ['id', 'blog_image']
        read_only_fields = ['id']

    def validate_blog_image(self, value):
        """Validate the blog image."""
        max_size = 5 * 1024 * 1024  # 5 MB
        valid_file_types = ['image/jpeg', 'image/png', 'image/gif']

        if value.size > max_size:
            raise serializers.ValidationError("Image size should be less than 5MB.")
        if value.content_type not in valid_file_types:
            raise serializers.ValidationError("Invalid file type. Allowed types: JPEG, PNG, GIF.")
        return value
