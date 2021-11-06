from rest_framework import serializers

from .marks_models import Tags


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Tags
