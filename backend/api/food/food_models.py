from django.db import models

from .marks_models import Tag
from api.users.models import User


class Product(models.Model):
    name = models.CharField(
        verbose_name="Название продукта",
        max_length=50,
        unique=True,
    )
    measurement_unit = models.CharField(
        verbose_name="Еденица измерения",
        max_length=10,
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ("name",)

    def __str__(self):
        return f"Наименование: {self.name} ({self.measurement_unit})"


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name="recipes",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
    )
    name = models.CharField(
        max_length=50,
        unique=True,
    )
    image = models.ImageField(
        verbose_name="Изображение",
        upload_to="recipes",
        help_text="Фотография готового блюда",
    )
    text = models.TextField(
        verbose_name="Описание рецепта",
        help_text="Как готовится это блюдо?",
        max_length=10000,
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name="Время приготовления в минутах",
        help_text="Сколько минут будет готовиться?",
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ("-pk",)

    def __str__(self):
        return (
            f"Блюдо: {self.name}, время готовки: {self.cooking_time},"
            f" рецепт: {self.text[:50]}"
        )


class Ingredient(models.Model):
    ingredient = models.ForeignKey(
        Product,
        verbose_name="Ингридиент",
        on_delete=models.CASCADE,
        related_name="ingredients",
    )
    amount = models.PositiveIntegerField(
        verbose_name="Количество",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredients",
    )

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"
        ordering = ("ingredient__name",)
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
