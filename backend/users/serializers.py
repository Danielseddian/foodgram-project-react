from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from ..food.food_models import Recipes
from .models import Follow, User

SELF_FOLLOWING = "Нельзя подписаться на себя"
FOLLOW_EXISTS = "Такая подписка уже существует"


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField("get_user_subscribe")

    class Meta:
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )
        model = User

    def get_user_subscribe(self, user):
        follower = self.context["request"].user
        follow = (
            True
            if follower.is_authenticated
            and Follow.objects.filter(
                following=user,
                follower=follower,
            )
            else False
        )
        return follow


class RecipesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "name", "image", "cooking_time")
        model = Recipes


class FollowSerializer(UserSerializer):
    recipes = RecipesSerializer(read_only=True, many=True, source="author")

    class Meta:
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
        )
        model = User


class FollowCreateDestroySerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if self.context["request"].user == attrs["following"]:
            raise ValidationError(SELF_FOLLOWING)
        return attrs

    class Meta:
        fields = "__all__"
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=["follower", "following"],
                message=FOLLOW_EXISTS,
            )
        ]
