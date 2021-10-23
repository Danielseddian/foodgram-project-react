from django_filters import rest_framework as filters

from .food_models import Recipes


class RecipesFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(method="get_favorited")
    is_in_shopping_cart = filters.BooleanFilter(method="get_shopping_cart")

    class Meta:
        model = Recipes
        fields = ["author", "tags", "is_favorited", "is_in_shopping_cart"]

    def get_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorite__owner=self.request.user)
        return Recipes.objects.all()

    def get_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return Recipes.objects.filter(buying__owner=self.request.user)
        return Recipes.objects.all()
