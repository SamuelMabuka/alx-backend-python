from pathlib import Path
from datetime import timedelta
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environ
env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")  # load variables from .env

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'oauth2_provider',
    'django_filters',   # needed for filtering support
    'chats',
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("MYSQL_DATABASE", default="messaging_db"),
        "USER": env("MYSQL_USER", default="messaging_user"),
        "PASSWORD": env("MYSQL_PASSWORD", default="messaging_pass"),
        "HOST": env("MYSQL_HOST", default="db"),  # docker-compose service name
        "PORT": env("MYSQL_PORT", default="3306"),
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'chats.pagination.MessagePagination',
    'PAGE_SIZE': 100,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

AUTH_USER_MODEL = 'chats.User'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}