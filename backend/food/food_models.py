from django.db import models
from users.models import User

from .marks_models import Tags


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
        return f"Наименование: {self.name} ({self.measurement_unit})"


class Recipes(models.Model):
    tags = models.ManyToManyField(
        Tags,
        null=False,
        blank=False,
        related_name="tag",
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
        null=False,
        blank=False,
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name="Время приготовления в минутах",
        help_text="Сколько минут будет готовиться?",
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
    amount = models.PositiveIntegerField(
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
