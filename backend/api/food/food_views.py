from rest_framework.viewsets import ModelViewSet

from .filters import IngredientFilter, RecipeFilter
from .food_models import Product, Recipe
from .food_serializers import RecipeSerializer, ProductSerializer
from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly


class IngredientViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = None
    filterset_class = IngredientFilter
    permission_classes = [IsAdminOrReadOnly]


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    filterset_class = RecipeFilter
    serializer_class = RecipeSerializer
    permission_classes = [IsAdminOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        if "tags" not in self.request.query_params and not self.kwargs:
            return self.queryset.none()
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            tags=self.request.data["tags"],
            ingredients=self.request.data["ingredients"],
        )

    def perform_update(self, serializer):
        serializer.save(
            author=self.request.user,
            tags=self.request.data['tags'],
            ingredients=self.request.data['ingredients']
        )
