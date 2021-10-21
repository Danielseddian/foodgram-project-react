from django.db import models

from ..users.models import User
from .food_models import Recipes


class ShoppingLists(models.Model):
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="buyer",
    )
    products = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="buying",
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


class Favorites(models.Model):
    admirer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="admirer",
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="favorite",
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
