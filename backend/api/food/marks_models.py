from colorfield.fields import ColorField
from django.db import models


class Tag(models.Model):
    name = models.CharField(
        verbose_name="Имя тега",
        max_length=100,
        unique=True,
    )
    color = ColorField(
        verbose_name="Цвет тега",
        default="#FFFFFF",
        unique=True,
    )
    slug = models.SlugField(
        verbose_name="slug",
        max_length=20,
        unique=True,
    )

    def __str__(self):
        return f"Имя {self.name}, цвет {self.color}, тег {self.slug}"
