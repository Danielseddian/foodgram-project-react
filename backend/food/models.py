from django.db import models

from ..users.models import User
from ..marks_and_lists.models import Tags


class Products(models.Model):
    name = models.CharField(
        verbose_name="Название продукта",
        max_length=50,
        blank=False,
        null=False,
        unique=True,
    )
    measurement_unit = models.CharField(
        verbose_name="Еденица измерения",
        max_length=10,
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ("pk",)

    def __str__(self):
        return f"Наименование: {self.name}, измерение: {self.measurement_unit}"


class Recipes(models.Model):
    tags = models.ManyToManyField(
        Tags,
        null=False,
        blank=False,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="author",
    )
    name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        unique=True,
    )
    image = models.ImageField(
        verbose_name="Изображение",
        upload_to="recipe/",
        blank=False,
        null=False,
        help_text="Фотография готового блюда",
    )
    text = models.TextField(
        verbose_name="Описание рецепта",
        help_text="Как готовится это блюдо?",
        max_length=10000,
    )
    cooking_time = models.DurationField(
        verbose_name="Время приготовления",
        help_text="Какое время будет готовиться?",
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ("pk",)

    def __str__(self):
        return (
            f"Блюдо: {self.name}, время готовки: {self.cooking_time},"
            f" рецепт: {self.text[:50]}"
        )


class Ingredients(models.Model):
    ingredient = models.ForeignKey(
        Products,
        verbose_name="Ингридиент",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField(
        verbose_name="Количество",
        max_length=20,
        blank=False,
        null=False,
    )
    recipe = models.ForeignKey(
        Recipes,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="ingredients",
    )

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"
        ordering = ("pk",)
        constraints = [
            models.UniqueConstraint(
                fields=["ingredient", "recipe"],
                name="uniq_ingredients",
            ),
        ]

    def __str__(self):
        return (
            f"Наименование {self.ingredient.name}, количество:"
            f" {self.amount} {self.ingredient.measurement_unit}"
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
            f"Ингридиент {self.product.reciepe.name} в списке покупок "
            f"у пользователя {self.buyer.username}"
        )
