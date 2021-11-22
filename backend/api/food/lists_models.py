from django.db import models

from .food_models import Recipe
from api.users.models import User


class ShoppingList(models.Model):
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="to_buy",
    )
    products = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="to_buy",
    )

    class Meta:
        verbose_name = "Список покупок для рецепта"
        verbose_name_plural = "Список покупок для рецептов"
        ordering = ("pk",)
        constraints = [
            models.UniqueConstraint(
                fields=["buyer", "products"],
                name="uniq_shopping_list",
            ),
        ]

    def __str__(self):
        return (
            f"Продукты для  {self.products.name} в списке покупок "
            f"у пользователя {self.buyer.username}"
        )


class Favorite(models.Model):
    admirer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="faforites",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorites",
    )

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        ordering = ("pk",)
        constraints = [
            models.UniqueConstraint(
                fields=["admirer", "recipe"],
                name="uniq_favorite",
            ),
        ]

    def __str__(self):
        return (
            f"Рецепт {self.recipe.name} в избранном у "
            f"пользователя {self.admirer.username}"
        )
