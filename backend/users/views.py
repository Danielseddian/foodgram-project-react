from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

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


class UserViewSet(
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FollowViewSet(ListModelMixin, viewsets.GenericViewSet):
    serializer_class = FollowSerializer

    def get_queryset(self):
        return self.request.user.follower


class FollowChangeSet(CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = FollowCreateDestroySerializer

    def get(self, request, *args, **kwargs):
        data = {
            "following": kwargs["user_id"],
            "follower": User.objects.get(id=3).id,
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def perform_create(self, serializer):
        serializer.save(
            following=get_object_or_404(
                User,
                id=self.kwargs["user_id"],
            ).username,
            follower=User.objects.get(id=3).username,  # self.request.user,
        )

    def delete(self, *args, **kwargs):
        get_object_or_404(
            self.request.user.follower,
            following__id=kwargs["user_id"],
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
