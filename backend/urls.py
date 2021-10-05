from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)


router_v1 = DefaultRouter()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router_v1.urls)),
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
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
