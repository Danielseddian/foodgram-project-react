from colorfield.fields import ColorField
from django.db import models


class tags(models.Model):
    name = models.CharField(
        verbose_name="Имя тега",
        max_length=100,
        unique=True,
        blank=False,
        null=False,
    )
    colour = ColorField(
        verbose_name="Цвет тега",
        default="#FFFFFF",
        unique=True,
        blank=False,
        null=False,
    )
    slug = models.SlugField(
        verbose_name="slug",
        max_length=20,
        unique=True,
        blank=False,
        null=False,
    )
