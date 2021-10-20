from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from .models import User, Follow

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


class FollowSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all(),
    )
    follower = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault,
    )

    class Meta:
        fields = "__all__"
        model = Follow


class FollowCreateDestroySerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        slug_field="id",
        queryset=User.objects.all(),
    )
    follower = serializers.SlugRelatedField(
        slug_field="id",
        queryset=User.objects.all(),
    )

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
