from django.urls import path
from . import views


urlpatterns = [
    path("category/", views.CategoryView.as_view(), name="category"),
    path(
        "category/<int:cat_id>/",
        views.CategoryViewID.as_view(),
        name="category-detail",
    ),
    path("user-category/", views.UserCategoryView.as_view(), name="user-category"),
    path(
        "user-category/<int:user_cat_id>/",
        views.UserCategoryViewID.as_view(),
        name="user-category-detail",
    ),
]
