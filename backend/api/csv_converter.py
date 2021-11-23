from os.path import dirname, abspath, join, exists
from csv import reader
from django.apps import apps

BASE_DIR = dirname(abspath(__file__))
PATH = "Укажи путь к файлу в формате: path/to/the/file_name.extantion:\n"
FILE_NOT_EXISTS = "Такой файл не существует. Укажи правильный путь к файлу:\n"
MODEL = ("Укажи через пробел приложение и модель для загрузки (пример: "
         "users User):\n")
MODEL_NOT_EXISTS = "В базе нет такой модели, попробуй ещё раз:"
FIELDS = ("Укажи через пробел поля, которые будут заполняться из таблицы или "
          "нажми ENTER, если поля указаны в файле:\n")
FIELDS_NOT_EXISTS = "В модели нет таких полей, укажи правильные:\n"


def csv_converter(file_name, model, fields):
    if fields:
        model_fields = [field.name for field in model._meta.get_fields()]
        fields = check_fields(fields.split(), model_fields)
    with open(file_name, encoding="utf8") as csv_file:
        for line in reader(csv_file):
            if not fields:
                fields = line
            else:
                print(dict(zip(fields, line)))


def check_path(path):
    if exists(path) and path != join(BASE_DIR, ""):
        return path
    else:
        return check_path(join(BASE_DIR, input(FILE_NOT_EXISTS)))


def check_model(data):
    try:
        app, name = data.split()
        return apps.get_model(app, name)
    except LookupError:
        return check_model(input(MODEL_NOT_EXISTS))


def check_fields(fields, model_fields):
    for field in fields:
        if field not in model_fields:
            return check_fields(input(FIELDS_NOT_EXISTS, model_fields))
    return fields


if __name__ == "__main__":
    path = check_path(join(BASE_DIR, input(PATH)))
    model = check_model(input(MODEL))
    fields = input(FIELDS)
    csv_converter(path, model, fields)
