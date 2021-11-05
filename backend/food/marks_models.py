from colorfield.fields import ColorField
from django.db import models


class Tags(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        verbose_name="Имя тега",
        max_length=100,
        unique=True,
        blank=False,
        null=False,
    )
    color = ColorField(
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

    def __str__(self):
        return f"Имя {self.name}, цвет {self.color}, тег {self.slug}"
