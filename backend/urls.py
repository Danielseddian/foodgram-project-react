from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .users.views import FollowViewSet, UserViewSet, FollowChangeSet


router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("subscriptions", FollowViewSet, basename="follows")
router.register(
    r"users/(?P<user_id>\d+)/subscriptions",
    FollowChangeSet,
    basename="subscribe",
)


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
