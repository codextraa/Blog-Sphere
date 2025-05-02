"""Views for blog api."""  # pylint: disable=C0302

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiResponse
from core_db.models import Category, User_Category
from backend.renderers import ViewRenderer
from .serializers import CategorySerializer, UserCategorySerializer


class CategoryView(APIView):
    """Category Get and Create View."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [ViewRenderer]

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = []
        return super().get_permissions()

    @extend_schema(
        summary="List Categories",
        description=(
            "List all categories. " "No authentication is required for this endpoint."
        ),
        request=None,
        responses={
            200: OpenApiResponse(
                description="Categories retrieved successfully.",
                response=CategorySerializer(many=True),
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        """List all the categories or retrieve a single category."""
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Create a Category",
        description=(
            "Create a new category. "
            "Only superusers can create categories. "
            "Requires authentication."
        ),
        request=CategorySerializer,
        responses={
            201: OpenApiResponse(
                description="Category created successfully.",
                response=CategorySerializer,
            ),
            400: OpenApiResponse(
                description="Invalid payload provided.",
                response={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "array",
                            "items": {"type": "string"},
                            "example": ["This field may not be blank."],
                        }
                    },
                },
            ),
            403: OpenApiResponse(
                description="User does not have permission to create a category.",
                response={
                    "type": "object",
                    "properties": {
                        "error": {
                            "type": "string",
                            "example": "You do not have permission to create a category.",
                        }
                    },
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        """Create a new category."""
        if not request.user.is_superuser:
            return Response(
                {"error": "You do not have permission to create a category."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewID(APIView):
    """Category Get and Delete View."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [ViewRenderer]

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = []
        return super().get_permissions()

    @extend_schema(
        summary="Retrieve User Categories",
        description=(
            "Retrieve a single user category by ID. "
            "No authentication is required for this endpoint."
        ),
        request=None,
        responses={
            200: OpenApiResponse(
                description="User Categories retrieved successfully.",
                response=UserCategorySerializer(),
            ),
            400: OpenApiResponse(
                description="User Category ID not provided.",
                response={
                    "type": "object",
                    "properties": {
                        "error": {
                            "type": "string",
                            "example": "User Category ID not provided.",
                        }
                    },
                },
            ),
            404: OpenApiResponse(
                description="Category not found.",
                response={
                    "type": "object",
                    "properties": {
                        "error": {
                            "type": "string",
                            "example": "Category not found",
                        }
                    },
                },
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        """List all the categories or retrieve a single category."""
        cat_id = kwargs.get("cat_id")

        if cat_id:
            try:
                category = Category.objects.get(id=cat_id)
                serializer = CategorySerializer(category)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Category.DoesNotExist:
                return Response(
                    {"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND
                )

        return Response(
            {"error": "Category ID not provided."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        summary="Delete a Category",
        description=(
            "Delete a category by ID. "
            "Only superusers can delete categories. "
            "Requires authentication."
        ),
        request=None,
        responses={
            204: OpenApiResponse(
                description="Category deleted successfully.",
                response=None,
            ),
            400: OpenApiResponse(
                description="Category ID not provided.",
                response={
                    "type": "object",
                    "properties": {
                        "error": {
                            "type": "string",
                            "example": "Category ID not provided.",
                        }
                    },
                },
            ),
            403: OpenApiResponse(
                description="User does not have permission to delete a category.",
                response={
                    "type": "object",
                    "properties": {
                        "error": {
                            "type": "string",
                            "example": "You do not have permission to delete a category.",
                        }
                    },
                },
            ),
            404: OpenApiResponse(
                description="Category not found.",
                response={
                    "type": "object",
                    "properties": {
                        "error": {
                            "type": "string",
                            "example": "Category not found",
                        }
                    },
                },
            ),
        },
    )
    def delete(self, request, *args, **kwargs):
        """Delete a category."""
        if not request.user.is_superuser:
            return Response(
                {"error": "You do not have permission to delete a category."},
                status=status.HTTP_403_FORBIDDEN,
            )

        cat_id = kwargs.get("cat_id")

        if cat_id:
            try:
                category = Category.objects.get(id=cat_id)
                category.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Category.DoesNotExist:
                return Response(
                    {"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND
                )

        return Response(
            {"error": "Category ID not provided."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserCategoryView(APIView):
    """User Category Create and Delete View."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [ViewRenderer]

    @extend_schema(
        summary="List User Categories",
        description=(
            "List all User Categories. "
            "No authentication is required for this endpoint."
        ),
        request=None,
        responses={
            200: OpenApiResponse(
                description="User Categories retrieved successfully.",
                response=UserCategorySerializer(many=True),
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        """List all the User Categories."""
        try:
            user_categories = User_Category.objects.filter(user=request.user)
            serializer = UserCategorySerializer(user_categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:  # pylint: disable=W0718
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(
        summary="Create a User Category",
        description=(
            "Create a new user category. "
            "Only superusers can create user categories. "
            "Requires authentication."
        ),
        request=UserCategorySerializer,
        responses={
            201: OpenApiResponse(
                description="User Category created successfully.",
                response=UserCategorySerializer,
            ),
            400: OpenApiResponse(
                description="Invalid payload provided.",
                response={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "array",
                            "items": {"type": "string"},
                            "example": ["This field may not be blank."],
                        }
                    },
                },
            ),
            403: OpenApiResponse(
                description="User does not have permission to delete a category.",
                response={
                    "type": "object",
                    "properties": {
                        "error": {
                            "type": "string",
                            "example": "You do not have permission to create "
                            "another user's  category.",
                        }
                    },
                },
            ),
            404: OpenApiResponse(
                description="User not found.",
                response={
                    "type": "object",
                    "properties": {
                        "error": {
                            "type": "string",
                            "example": "User not found",
                        }
                    },
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        """Create a new user category."""
        user_id = request.data["user"]
        try:
            user = get_user_model().objects.get(id=user_id)
        except get_user_model().DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if request.user.id != user.id:
            return Response(
                {
                    "error": "You do not have permission to create another user's category."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = UserCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCategoryViewID(APIView):
    """User Category Get and Delete View."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [ViewRenderer]

    @extend_schema(
        summary="Delete a User Category",
        description=(
            "Delete a User category by ID. "
            "Only superusers can delete user categories. "
            "Requires authentication."
        ),
        request=None,
        responses={
            204: OpenApiResponse(
                description="User Category deleted successfully.",
                response=None,
            ),
            400: OpenApiResponse(
                description="User Category ID not provided.",
                response={
                    "type": "object",
                    "properties": {
                        "error": {
                            "type": "string",
                            "example": "User category ID not provided.",
                        }
                    },
                },
            ),
            403: OpenApiResponse(
                description="User does not have permission to delete a category.",
                response={
                    "type": "object",
                    "properties": {
                        "error": {
                            "type": "string",
                            "example": "You do not have permission to delete a user category.",
                        }
                    },
                },
            ),
            404: OpenApiResponse(
                description="User category not found.",
                response={
                    "type": "object",
                    "properties": {
                        "error": {
                            "type": "string",
                            "example": "User category not found",
                        }
                    },
                },
            ),
        },
    )
    def delete(self, request, *args, **kwargs):
        """Delete a user category."""
        user_cat_id = kwargs.get("user_cat_id")

        if not user_cat_id:
            return Response(
                {"error": "User category ID not provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_category = User_Category.objects.get(id=user_cat_id)
        except User_Category.DoesNotExist:
            return Response(
                {"error": "User category not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.user.id != user_category.user.id:
            return Response(
                {"error": "You do not have permission to delete a user category."},
                status=status.HTTP_403_FORBIDDEN,
            )

        user_category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
