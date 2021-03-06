"""
Django settings for blueweather project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import logging.config
import os

from .config import Config
from .plugins import Extensions
from .plugins import dao

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGGING_CONFIG = None
logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'brief': {
            'format': '%(levelname)-5.5s [%(asctime)s - %(name)s] %(message)s',
            'datefmt': '%I:%M:%S %p'
        },
        'default': {
            'format': '%(levelname)-5.5s [%(asctime)s - %(name)s] %(message)s',
            'datefmt': '%m/%d/%Y %I:%M:%S %p'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'brief',
            'level': 'INFO',
            'stream': 'ext://sys.stdout'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console']
    },
    #  'incremental': True
})

# Configuration are user-defined settings. They are all stored in the CONFIG
# object, and follow a different convention from Settings to differentiate them
CONFIG = Config(os.path.join(BASE_DIR, "config.yml"))
CONFIG.load()

# because django is set to reload, two instances of extensions will always be
# loaded. to stop this, use 'manage.py runserver --noreload'
EXTENSIONS = Extensions(CONFIG, True)
dao.Settings.load_settings(EXTENSIONS.settings, CONFIG)
if CONFIG.modified:
    CONFIG.save()


# Unit Conversions
UNITS = dao.UnitConversion.all_conversions(EXTENSIONS.unitConversion)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

SECRET_KEY = CONFIG.web.secret_key
DEBUG = CONFIG.web.debug
ALLOWED_HOSTS = CONFIG.web.allowed_hosts

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blueweather.apps.weather',
    'blueweather.apps.accounts',
    'blueweather.apps.plugins',
    'blueweather.apps.api',
    'blueweather.apps.settings'
]

# A list of apps that should be linked in the sidebar
SIDEBAR = CONFIG.web.sidebar

MODEL_SETTINGS = [
    'blueweather.apps.api.model_loaders.model_settings'
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware'
]

ROOT_URLCONF = 'blueweather.urls'

NPM_FILE_PATERNS = {
    'startbootstrap-sb-admin-2': [
        'css/*.min.css',
        'js/*.min.js',
        'scss/*'
    ]
}

STATIC_ROOT = "dist"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'npm.finders.NpmFinder'
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [
            os.path.join(BASE_DIR, "templates")
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            "environment": "blueweather.jinja2.environment",
            "context_processors": [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blueweather.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': CONFIG.web.database.get_data(BASE_DIR)
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = CONFIG.web.time_zone

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
