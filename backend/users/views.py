from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
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
    pass


class UserViewSet(ListViewSet, CreateModelMixin, RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FollowViewSet(ListViewSet):
    serializer_class = FollowSerializer

    def get_queryset(self):
        return self.request.user.follower


class FollowChangeSet(CreateModelMixin, GenericViewSet):
    serializer_class = FollowCreateDestroySerializer

    def get(self, request, *args, **kwargs):
        request.data["following"] = kwargs["user_id"]
        request.data["follower"] = 2  # self.request.user.id
        # data = self.create(request, *args, **kwargs)
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
