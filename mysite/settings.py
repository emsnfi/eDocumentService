"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 1.8.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import mysite.env
mysite.env.set()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["eDocumentService_SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
import socket
if socket.gethostname() == 'edspro':
    DEBUG = False
else:
    DEBUG = True


if socket.gethostname() == 'edspro':
    SECURE_SSL_REDIRECT = True

ALLOWED_HOSTS = ['*']

ADMINS = [
    ('eDocumentService', 'edocumentservice@gmail.com'),
]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ebookSystem',
    'genericUser',
    'rest_framework',
    #'rules',
    'rules.apps.AutodiscoverRulesConfig',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DB_BACKEND = os.environ.get('eDocumentService_DB_BACKEND')
if DB_BACKEND == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('eDocumentService_DATABASE'),
            'USER': os.environ.get('eDocumentService_DB_USER'),
            'PASSWORD': os.environ.get('eDocumentService_DB_PASS'),
            'HOST': os.environ.get('eDocumentService_DB_HOST'),
            'PORT': os.environ.get('eDocumentService_DB_PORT'),
        }
    }
elif DB_BACKEND == 'sqlite3':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
LOGIN_URL = '/auth/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/'
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
FILE_CHARSET='utf-8'
AUTH_USER_MODEL = 'genericUser.User'

'''CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}'''

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

'''CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}'''

from django.conf import global_settings
FILE_UPLOAD_HANDLERS = ['utils.cache.UploadProgressCachedHandler', ] + global_settings.FILE_UPLOAD_HANDLERS
#FILE_UPLOAD_HANDLERS = ('utils.uploadFile.ProgressUploadSessionHandler', ) + global_settings.FILE_UPLOAD_HANDLERS

if socket.gethostname() == 'edspro':
	EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
	EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(message)s\t%(levelname)s\t%(asctime)s\t%(module)s\t%(process)d\t%(thread)d'
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'formatter': 'verbose',
            'class': 'logging.FileHandler',
            'filename': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'log') +'/djangoOS.log',
        },
        'rotating_file':
        {
            'level' : 'DEBUG',
            'formatter' : 'verbose',
            'class' : 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'log') +'/djangoOS_rotate.log',
            'when' : 'midnight',
            'interval' : 1,
            'backupCount' : 7,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'rotating_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

#RECAPTCHA
#RECAPTCHA_PUBLIC_KEY
RECAPTCHA_PUBLIC_KEY = '6LemWCUTAAAAAN7vPBat6CikMrI1F2jOOmnV_XhO'
RECAPTCHA_PRIVATE_KEY = '6LemWCUTAAAAAC0N7Q9z9aH-yE2y08-BLECTelv_'
NOCAPTCHA = False
#CAPTCHA_AJAX = True

DEFAULT_FROM_EMAIL = 'edocumentservice@gmail.com'
MANAGER = ['edocumentservice@gmail.com']
SERVICE = 'edocumentservice@gmail.com'
TIME_ZONE = 'Asia/Taipei'

AUTHENTICATION_BACKENDS = (
    'rules.permissions.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    )
}

BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

OTP_ACCOUNT = os.environ["eDocumentService_OTP_ACCOUNT"]
OTP_PASSWORD = os.environ["eDocumentService_OTP_PASSWORD"]

EMAIL_HOST = os.environ["eDocumentService_EMAIL_HOST"]
EMAIL_PORT = os.environ["eDocumentService_EMAIL_PORT"]
EMAIL_HOST_USER = os.environ["eDocumentService_EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["eDocumentService_EMAIL_HOST_PASSWORD"]
EMAIL_USE_TLS = True
SERVICE = EMAIL_HOST_USER
