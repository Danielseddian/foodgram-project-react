from django.db import models

from ..users.models import User
from .food_models import Recipes, Ingredients


class ShoppingLists(models.Model):
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="buyer",
    )
    product = models.ForeignKey(
        Ingredients,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="to_shop",
    )

    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"
        ordering = ("pk",)
        constraints = [
            models.UniqueConstraint(
                fields=["buyer", "product"],
                name="uniq_purchase",
            ),
        ]

    def __str__(self):
        return (
            f"Ингридиент {self.product.recipe.name} в списке покупок "
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
