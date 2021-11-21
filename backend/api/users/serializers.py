from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.validators import UniqueTogetherValidator

from .models import Follow, User
from api.food.food_models import Recipe

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
        request = self.context.get("request")
        if not request:
            return False
        follower = request.user
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
        extra_kwargs = {"password": {"write_only": True}}
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
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


class GetRecipeSerializer(serializers.ModelSerializer):
    image = SerializerMethodField()

    class Meta:
        fields = ("id", "name", "image", "cooking_time")
        model = Recipe

    def get_image(self, obj):
        return obj.image.url


class FollowSerializer(UserSerializer):
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )
        model = User

    def get_recipes(self, obj, limit="recipes_limit"):
        request = self.context.get("request")
        params = request.query_params if request else None
        recipes = Recipe.objects.filter(author=obj)
        recipes = recipes[: int(params[limit])] if limit in params else recipes
        return GetRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()


class FollowCreateDestroySerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        request = self.context.get("request")
        if request and request.user == attrs["following"]:
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
