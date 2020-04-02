"""
Django settings for wedding project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import json
from django.core.exceptions import ImproperlyConfigured


class DictObj:
    def __init__(self, dct):
        for k, v in dct.items():
            if isinstance(v, dict):
                self.__dict__[k] = DictObj(v)
            else:
                self.__dict__[k] = v

    def __getattr__(self, item):
        if item in self.__dict__.keys():
            return object.__getattribute__(self, item)
        else:
            raise ImproperlyConfigured('Key {} not found in {} environment config file.'.format(item, ENV))

    def get(self, item, default='Unspecified'):
        if item in self.__dict__.keys():
            return getattr(self, item)
        else:
            # Using a string value here since we may want some keys to return None
            if default is not 'Unspecified':
                return default


ENV = 'dev'  # dev|test|prod

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dynamically load environment-specific config files
"""
Each environment as defined by ENV must have an associated configuration file located in BASE_DIR called one of:

 - .dev.settings.json
 - .test.settings.json
 - .prod.settings.json
 
This is intended to conceal sensitive information from public repositories, like the Django secret, DB creds and keys.
This also allows for some environment-specific configuration, like switching between database engines.
"""
CONFIG_FILE = os.path.join(BASE_DIR, '.{}.settings.json'.format(ENV))

cfg_contents = {} if not os.path.exists(CONFIG_FILE) else json.load(open(CONFIG_FILE, 'r'))
CONFIG = DictObj(cfg_contents)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONFIG.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if ENV is 'dev' else False

if ENV is 'dev':
    ALLOWED_HOSTS = []
elif ENV is 'test':
    ALLOWED_HOSTS = ['rgk.pythonanywhere.com', 'wedding.rkstage.com', '127.0.0.1', 'localhost']
elif ENV is 'prod':
    ALLOWED_HOSTS = ['kathrynandrob.com', 'www.kathrynandrob.com']


# Application definition

INSTALLED_APPS = [
    'wedding.apps.WeddingConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'wedding.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'wedding.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.{}'.format(CONFIG.DB.ENGINE),
        'NAME': CONFIG.DB.NAME,
        'USER': CONFIG.DB.get('USER', ''),
        'PASSWORD': CONFIG.DB.get('PASSWORD', ''),
        'HOST': CONFIG.DB.get('HOST', ''),
        'PORT': CONFIG.DB.get('PORT', ''),
    },
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

TIME_ZONE = CONFIG.get('TIMEZONE', 'America/New_York')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = CONFIG.get('STATIC_ROOT', '')
STATIC_URL = CONFIG.get('STATIC_URL', '/static/')

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'static/'),
)
