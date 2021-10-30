from django.contrib.auth.models import AbstractUser

from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )
    first_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
    )
    is_admin = models.BooleanField(
        verbose_name="Администратор",
        default=False,
    )

    def __str__(self):
        return (
            f"Пользователь {self.username}: email: {self.email}"
            f", имя: {self.last_name} {self.first_name}"
        )


class Follow(models.Model):
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
    )
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ("pk",)
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"],
                name="uniq_follow",
            ),
            models.CheckConstraint(
                check=~models.Q(follower=models.F("following")),
                name="follower_is_not_following",
            ),
        ]

    def __str__(self):
        return (
            f"Пользователь {self.follower.username} подписан "
            f"на пользователя {self.following.username}"
        )
