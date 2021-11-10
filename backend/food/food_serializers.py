from drf_extra_fields.fields import Base64ImageField
from foodgram.settings import STATIC_ROOT
from rest_framework.serializers import CharField, ModelSerializer, SerializerMethodField
from users.serializers import UserSerializer

from .food_models import Ingredients, Products, Recipes
from .lists_models import Favorites, ShoppingLists
from .marks_serializers import TagsSerializer


class ProductsSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Products


class IngredientSerializer(ModelSerializer):
    name = CharField(read_only=True, source="ingredient.name")
    measurement_unit = CharField(
        read_only=True,
        source="ingredient.measurement_unit",
    )

    class Meta:
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )
        model = Ingredients


"""
class Base64ImageField(ImageField):

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension"""


class RecipesSerializer(ModelSerializer):
    tags = TagsSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    is_favorited = SerializerMethodField("check_is_favorite")
    is_in_shopping_cart = SerializerMethodField("check_in_user_shopping_cart")
    image = Base64ImageField()

    class Meta:
        fields = "__all__"
        model = Recipes

    def check_is_favorite(self, obj):
        admirer = self.context["request"].user
        favorite = (
            True
            if admirer.is_authenticated
            and Favorites.objects.filter(
                recipe=obj.id,
                admirer=admirer.id,
            )
            else False
        )
        return favorite

    def check_in_user_shopping_cart(self, obj):
        buyer = self.context["request"].user
        is_in_shopping_cart = (
            True
            if buyer.is_authenticated
            and ShoppingLists.objects.filter(
                products=obj.id,
                buyer=buyer.id,
            )
            else False
        )
        return is_in_shopping_cart

    def get_image(self, obj):
        print(obj.image.read().decode())
        return STATIC_ROOT + obj.image.name


class RecipeAddSerializer(RecipesSerializer):
    author = UserSerializer(read_only=True)
    image = Base64ImageField()

    class Meta:
        fields = [
            "id",
            "tags",
            "name",
            "image",
            "cooking_time",
            "text",
            "author",
        ]
        model = Recipes
