from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .users.views import FollowViewSet, UserViewSet, FollowChangeSet
from .food.views import (
    ChangeShoppingListViewSet,
    RecipesViewSet,
    TagsViewSet,
    IngredientsViewSet,
    FavoriteViewSet,
)


router = DefaultRouter()
router.register("users/subscriptions", FollowViewSet, basename="follows")
router.register("users", UserViewSet, basename="users")
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
    path(
        "token/",
        TokenObtainPairView.as_view(),
        name="token_obtain",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(r"^auth", include("djoser.urls")),
    path(r"^auth", include("djoser.urls.authtoken")),
]
