from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from food.views import (
    ChangeShoppingListViewSet,
    FavoriteViewSet,
    IngredientsViewSet,
    RecipesViewSet,
    TagsViewSet,
)
from users.views import FollowChangeSet, FollowViewSet

router = DefaultRouter()
router.register("users/subscriptions", FollowViewSet, basename="follows")
router.register(
    r"users/(?P<user_id>\d+)/subscriptions",
    FollowChangeSet,
    basename="subscribe",
)
router.register("recipes", RecipesViewSet, basename="recipes")
router.register(
    r"recipes/(?P<favorite_id>\d+)/favorite",
    FavoriteViewSet,
    basename="subscribe",
)
router.register(
    r"recipes/(?P<buying_id>\d+)/shopping_cart",
    ChangeShoppingListViewSet,
    basename="shopping_cart",
)
router.register("tags", TagsViewSet, basename="tags")
router.register("ingredients", IngredientsViewSet, basename="ingredients")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
]
