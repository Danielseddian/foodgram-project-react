from food.food_models import Recipes
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

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


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
        )
        model = User

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class GetRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "name", "image", "cooking_time")
        model = Recipes


class FollowSerializer(UserSerializer):
    recipes = GetRecipesSerializer(read_only=True, many=True, source="author")

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
