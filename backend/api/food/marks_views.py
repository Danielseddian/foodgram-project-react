from django_filters import rest_framework as rest_filters
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsAdminOrReadOnly

from .marks_models import Tag
from .marks_serializers import TagSerializer


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None
    filter_backends = [rest_filters.DjangoFilterBackend]
    filterset_fields = ["name", "slug"]
    permission_classes = [IsAdminOrReadOnly]
