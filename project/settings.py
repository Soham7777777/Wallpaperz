"""
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
import django
from dotenv import load_dotenv


load_dotenv()


def env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ValueError(f'The environment variable {key} is not set.')
    return value


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS: list[str] = []

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin.apps.SimpleAdminConfig',
    'common',
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            django.__path__[0] + '/forms/templates',
            django.__path__[0] + '/contrib/admin/templates',
            django.__path__[0] + '/contrib/auth/templates',
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'django.contrib.auth.context_processors.auth',
            ],
        },
    },
]

FORM_RENDERER = 'project.forms.renderers.BootstrapFormRendered'

WSGI_APPLICATION = 'project.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Static files

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_URL = 'static/'


# Uploaded files

MEDIA_ROOT = BASE_DIR / 'uploads'

MEDIA_URL = 'media/'
