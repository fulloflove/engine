"""
Django settings for engine project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from __future__ import absolute_import
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')
TEMPLATE_DIRS = [
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    TEMPLATE_PATH,
]

# Domain URL
BASE_URL = 'http://hd.factormsk.ru'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3us+=_xj1f59s(z_@hs1w=+(c+n@1mq022u!x=g5@ukaxurnu6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'widget_tweaks',
    'haystack',
    'regions',
    'helpdesk',
    'djcelery'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'engine.urls'

WSGI_APPLICATION = 'engine.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cbr',
        'USER': 'postgres',
        'PASSWORD': '1qaz!QAZ',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },
    'legacy': {
        'NAME': 'requestengine',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': '1qaz!QAZ',
        'HOST': '192.168.51.192',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_INPUT_FORMATS = (
    '%d.%m.%Y', '%d.%m.%y',  # '25.10.2006', '25.10.06'
    '%d-%m-%Y', '%d/%m/%Y', '%d/%m/%y',  # '25-10-2006', '25/10/2006', '25/10/06'
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_PATH = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    STATIC_PATH,
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Absolute path to the media directory

LOGIN_URL = 'helpdesk:login'
LOGIN_REDIRECT_URL = 'helpdesk:index'

# SMTP settings for sending e-mails
EMAIL_HOST = 'dionis.factor-ts.ru'
EMAIL_PORT = 25
EMAIL_ADDRESS = 'no-reply@hd.factormsk.ru'

# Haystack settings
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}

# Celery settings
from celery.schedules import crontab

BROKER_URL = 'amqp://127.0.0.1:5672'
CELERY_RESULT_BACKEND = 'amqp://127.0.0.1:5672'

CELERYBEAT_SCHEDULE = {
    'issue_info_morning': {
        'task': 'helpdesk.tasks.issue_info_morning',
        'schedule': crontab(minute=0, hour=9)
    },
    'issue_info_afternoon': {
        'task': 'helpdesk.tasks.issue_info_afternoon',
        'schedule': crontab(minute=0, hour=14),
    },
    'issue_warning': {
        'task': 'helpdesk.tasks.issue_warning',
        'schedule': crontab(minute=0, hour=13),
    },
}

# Pagination
ENTRIES_PER_PAGE = 25