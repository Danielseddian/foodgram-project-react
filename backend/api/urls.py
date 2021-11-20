from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .food.food_views import IngredientViewSet, RecipeViewSet
from .food.lists_views import (ChangeShoppingListViewSet, DownloadShoppingCart,
                               FavoriteViewSet)
from .food.marks_views import TagViewSet
from .users.views import FollowChangeSet, FollowViewSet

router = DefaultRouter()
router.register("users/subscriptions", FollowViewSet, basename="follows")
router.register(
    r"users/(?P<user_id>\d+)/subscribe",
    FollowChangeSet,
    basename="subscribe",
)
router.register("recipes", RecipeViewSet, basename="recipes")
router.register(
    r"recipes/(?P<recipe_id>\d+)/favorite",
    FavoriteViewSet,
    basename="subscribe",
)
router.register(
    r"recipes/(?P<recipe_id>\d+)/shopping_cart",
    ChangeShoppingListViewSet,
    basename="shopping_cart",
)
router.register("tags", TagViewSet, basename="tags")
router.register("ingredients", IngredientViewSet, basename="ingredients")


urlpatterns = [
    path("recipes/download_shopping_cart/", DownloadShoppingCart.as_view()),
    path("", include(router.urls)),
    path("", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
]
