from rest_framework.exceptions import ValidationError

from .food_models import Product

LITTLE_TIME = "На всё требуется время. Хотя бы одна минута"
MISSING_AMOUNT = "Так ничего не приготовить — требуется больше ингредиента."
MISSING_INGREDIENT = "Необходим хоть один ингредиет."
MISSING_TAGS = "Необходимо отметить хоть один тег."
UNIQ_TAGS = "Теги нельзя указывать дважды."
WRONG_PRODUCT = "Такого ингредиента пока нет, но, возможно, скоро появится."


def validate_cooking_time(data):
    context = data.get("request")
    if int(context.data.get("cooking_time")) < 1:
        raise ValidationError(LITTLE_TIME)
    return data


def validate_ingredients(data):
    amounts = {}
    if not data:
        raise ValidationError(MISSING_INGREDIENT)
    for ingredient in data:
        amount = int(ingredient["amount"])
        if amount < 1:
            raise ValidationError(MISSING_AMOUNT)
        pk = int(ingredient["id"])
        amounts[pk] = amounts[pk] + amount if pk in amounts else amount
    products = Product.objects.filter(id__in=amounts)
    values = [pk["id"] for pk in products.values("id")]
    if amounts.keys() - values:
        raise ValidationError(WRONG_PRODUCT)
    return amounts, products


def validate_tags(data):
    if not data:
        raise ValidationError(MISSING_TAGS)
    if len(data) != len(set(data)):
        raise ValidationError(UNIQ_TAGS)
    return data
