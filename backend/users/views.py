from rest_framework import status  # , permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)

from .models import User
from .serializers import (
    UserSerializer,
    FollowSerializer,
    FollowCreateDestroySerializer,
)


class ListViewSet(GenericViewSet, ListModelMixin):
    pagination_class = PageNumberPagination
    pass


class UserViewSet(ListViewSet, CreateModelMixin, RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FollowViewSet(ListViewSet):
    serializer_class = FollowSerializer

    def get_queryset(self):
        return User.objects.filter(following__follower=self.request.user.id)


class FollowChangeSet(CreateModelMixin, GenericViewSet):
    serializer_class = FollowCreateDestroySerializer
    # permission_classes = permissions.IsAuthenticated

    def get(self, request, *args, **kwargs):
        request.data["following"] = kwargs["user_id"]
        request.data["follower"] = 2  # self.request.user.id
        return self.create(request, *args, **kwargs)

    def delete(self, *args, **kwargs):
        get_object_or_404(
            get_object_or_404(
                User,
                id=2,
            ).follower,  # self.request.user.follower,
            following__id=kwargs["user_id"],
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
