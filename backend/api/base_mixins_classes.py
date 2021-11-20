from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet


class CreateView(GenericViewSet, CreateModelMixin):
    pass
