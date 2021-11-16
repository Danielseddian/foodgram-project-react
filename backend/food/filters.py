from django_filters import rest_framework as filters
from django_filters.filters import (AllValuesFilter, AllValuesMultipleFilter,
                                    CharFilter)

from .food_models import Products, Recipes


class RecipesFilter(filters.FilterSet):
    author = AllValuesFilter(
        method="get_user_recipes",
    )
    tags = AllValuesMultipleFilter(
        method="get_taged_recipes",
        field_name="tags__slug",
    )
    is_favorited = filters.BooleanFilter(method="get_favorited")
    is_in_shopping_cart = filters.BooleanFilter(method="get_shopping_cart")

    class Meta:
        model = Recipes
        fields = ["author", "tags", "is_favorited", "is_in_shopping_cart"]

    def get_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorite__admirer=self.request.user)
        return queryset

    def get_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return Recipes.objects.filter(buying__buyer=self.request.user)
        return queryset

    def get_taged_recipes(self, queryset, name, tags):
        """Пустой список, чтобы без тегов ничего не отображалось, заменяется и
        и фильтруется по тегам или фильтруется список от других фильтров"""
        queryset = (
            queryset.filter(tags__slug__in=tags).distinct("pk")
            if queryset
            else Recipes.objects.filter(tags__slug__in=tags).distinct("pk")
        )
        return queryset

    def get_user_recipes(self, queryset, name, pk):
        return Recipes.objects.filter(author__id__in=pk)


class IngredientsFilter(filters.FilterSet):
    name = CharFilter(method="name_filter")

    class Meta:
        model = Products
        fields = ("name",)

    def name_filter(self, queryset, name, value):
        return queryset.filter(name__icontains=value)
