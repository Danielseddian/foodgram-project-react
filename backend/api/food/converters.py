from base64 import b64decode
from django.core.files.base import ContentFile
from django.http import HttpResponse
from imghdr import what
from rest_framework.serializers import ImageField
from six import string_types
from uuid import uuid4

WRONG_IMAGE_TYPE = "Изображение не соответствует"
BASE64 = ";base64,"


class Base64ImageField(ImageField):
    def to_internal_value(self, data):
        if isinstance(data, string_types):
            if "data:" in data and BASE64 in data:
                header, data = data.split(BASE64)
            try:
                decoded_file = b64decode(data)
            except TypeError:
                self.fail(WRONG_IMAGE_TYPE)
            file_name = str(uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension)
            data = ContentFile(decoded_file, name=complete_file_name)
        return super().to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        extension = what(file_name, decoded_file)
        return "jpg" if extension == "jpeg" else extension


def get_content(ingredients, name_field, measure_field, amount_field):
    products = {}
    for ingredient in ingredients:
        name, measurement, amount = (
            ingredient[name_field],
            ingredient[measure_field],
            ingredient[amount_field],
        )
        product = name + f" ({measurement}) — "
        if product in products:
            products[product] += amount
        else:
            products[product] = amount
    content = ""
    for product in products:
        content += product + str(products[product]) + "\n"
    response = HttpResponse(content, content_type="text/plain")
    response["Content-Disposition"] = "attachment; filename=to_buy.txt"
    return response
