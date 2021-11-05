from os import environ
from os.path import abspath, dirname, exists, join

from dotenv import load_dotenv

context_processors = "django.template.context_processors."
contrib = "django.contrib."
middleware = "django.middleware."
pagination = "rest_framework.pagination."
password_validation = contrib + "auth.password_validation."
permissions = "rest_framework.permissions."
throttling = "rest_framework.throttling."

BASE_DIR = dirname(dirname(abspath(__file__)))

dotenv_path = join(BASE_DIR, ".env")
if exists(dotenv_path):
    load_dotenv(dotenv_path)

django_apps = [
    contrib + "contenttypes",
    contrib + "sessions",
    contrib + "messages",
    contrib + "staticfiles",
    contrib + "admin",
    contrib + "auth",
    "django_filters",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
]

local_apps = [
    "users",
    "food",
    "foodgram",
    "api",
]

others_apps = [
    "djoser",
    "colorfield",
]

INSTALLED_APPS = django_apps + local_apps + others_apps

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        permissions + "IsAuthenticated",
        permissions + "AllowAny",
        permissions + "IsAdminUser",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        throttling + "UserRateThrottle",
        throttling + "AnonRateThrottle",
        throttling + "ScopedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "user": "10000/minute",
        "anon": "100/minute",
    },
    "DEFAULT_PAGINATION_CLASS": pagination + "LimitOffsetPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
}

DJOSER = {
    "SERIALIZERS": {
        "user": "users.serializers.UserSerializer",
        "user_create": "users.serializers.UserCreateSerializer",
        "current_user": "users.serializers.UserSerializer",
    },
    "PERMISSIONS": {"user_list": [permissions + "AllowAny"]},
    "LOGIN_FIELD": "email",
    "HIDE_USERS": False,
}


MIDDLEWARE = [
    middleware + "security.SecurityMiddleware",
    contrib + "sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    middleware + "common.CommonMiddleware",
    middleware + "csrf.CsrfViewMiddleware",
    contrib + "auth.middleware.AuthenticationMiddleware",
    contrib + "messages.middleware.MessageMiddleware",
    middleware + "clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                context_processors + "debug",
                context_processors + "request",
                contrib + "auth.context_processors.auth",
                contrib + "messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": environ.get(
            "DB_ENGINE",
            "django.db.backends.postgresql_psycopg2",
        ),
        "NAME": environ.get("DB_NAME"),
        "USER": environ.get("POSTGRES_USER"),
        "PASSWORD": environ.get("POSTGRES_PASSWORD"),
        "HOST": environ.get("DB_HOST"),
        "PORT": environ.get("DB_PORT"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": password_validation + "UserAttributeSimilarityValidator",
    },
    {
        "NAME": password_validation + "MinimumLengthValidator",
    },
    {
        "NAME": password_validation + "CommonPasswordValidator",
    },
    {
        "NAME": password_validation + "NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

CORS_ORIGIN_ALLOW_ALL = True

CORS_URLS_REGEX = r"^/api/.*$"

STATIC_URL = "/static/"

STATIC_ROOT = join(BASE_DIR, "static")

MEDIA_URL = "/media/"

MEDIA_ROOT = join(BASE_DIR, "media")

SECRET_KEY = environ.get("SECRET_KEY", "some_secret_key")

DEBUG = environ.get("DEBUG", False)

ALLOWED_HOSTS = environ.get("ALLOWED_HOSTS", "localhost web").split()

AUTH_USER_MODEL = "users.User"

WSGI_APPLICATION = "foodgram.wsgi.application"

ROOT_URLCONF = "foodgram.urls"
