from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register
from core_db.models import User, Blog, Category, Blog_Category
from django.db.models import Prefetch


@register(User)
class UserIndex(AlgoliaIndex):
    name = "sphere_users"
    custom_objectID = "id"  # Using id as the unique identifier
    fields = (
        "email",
        "username",
        "first_name",
        "last_name",
        "bio",
    )
    settings = {
        "searchableAttributes": ["email", "username", "first_name", "last_name", "bio"],
        "attributesForFaceting": ["username"],
        "typoTolerance": {
            "minCharToAcceptOneTypo": 4,
            "minCharToAcceptTwoTypos": 8,
        },
        "wordProximity": 1,
    }

    def get_queryset(self):
        """Return the queryset for indexing all users."""
        return self.model.objects.only(
            "email", "username", "first_name", "last_name", "bio"
        )


@register(Blog)
class BlogIndex(AlgoliaIndex):
    name = "sphere_blogs"
    custom_objectID = "id"  # Using id as the unique identifier
    fields = (
        "title",
        "overview",
        "content",
        ("author_email", lambda obj: obj.author.email),
        ("author_username", lambda obj: obj.author.username),
        ("author_first_name", lambda obj: obj.author.first_name),
        ("author_last_name", lambda obj: obj.author.last_name),
        (
            "category_names",
            lambda obj: list(obj.categories.values_list("category__name", flat=True)),
        ),
        "status",
        "score",
    )
    settings = {
        "searchableAttributes": [
            "title",
            "overview",
            "content",
            "author_email",
            "author_username",
            "author_first_name",
            "author_last_name",
            "category_names",
        ],
        "attributesForFaceting": [
            "author_first_name",
            "author_last_name",
            "author_username",
            "category_names",
            "status",
        ],
        "typoTolerance": {
            "minCharToAcceptOneTypo": 4,
            "minCharToAcceptTwoTypos": 8,
        },
        "wordProximity": 1,
        "customRanking": ["desc(score)"],
    }

    def get_queryset(self):
        """Return the queryset for indexing only published blogs with optimized loading."""
        return self.model.objects.filter(status="Published").prefetch_related(
            Prefetch(
                "categories", queryset=Blog_Category.objects.select_related("category")
            )
        )


@register(Category)
class CategoryIndex(AlgoliaIndex):
    name = "sphere_categories"
    custom_objectID = "id"  # Using id as the unique identifier
    fields = ("name",)
    settings = {
        "searchableAttributes": ["name"],
        "attributesForFaceting": ["name"],
        "typoTolerance": {
            "minCharToAcceptOneTypo": 4,
            "minCharToAcceptTwoTypos": 8,
        },
        "wordProximity": 1,
    }

    def get_queryset(self):
        """Return the queryset for indexing all categories."""
        return self.model.objects.only("name")
