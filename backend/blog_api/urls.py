from django.urls import path
from . import views


urlpatterns = [
    path("category/", views.CategoryView.as_view(), name="category"),
    path("user-category/", views.UserCategoryView.as_view(), name="user-category"),
    path(
        "user-category/retrieve/",
        views.UserCategoryRetrieveView.as_view(),
        name="user-category-retrieve",
    ),
]
