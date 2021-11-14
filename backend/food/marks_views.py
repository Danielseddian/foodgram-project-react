from django_filters import rest_framework as rest_filters
from rest_framework import permissions

from .food_views import ListRetriveView
from .marks_models import Tags
from .marks_serializers import TagsSerializer


class TagsViewSet(ListRetriveView):
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()
    pagination_class = None
    filter_backends = [rest_filters.DjangoFilterBackend]
    filterset_fields = ["name", "slug"]
    permission_classes = [permissions.AllowAny]
