"""
Django settings for local configuration.

This file is used as base for all configurations. It is copied to
<configurationKey>-settings.py and the configuration key is swapped with the
actual configuration key.

Edit the appropriate configuration file instead of this file.
"""

from pathlib import Path
from datetime import timedelta
import os

import django
from django.utils.encoding import force_str
django.utils.encoding.force_text = force_str

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-jz4%bt0*ninfa7p@g4&_431s#upnn8_u16_9^rl_x(9pqckaq_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# EMAIL_BACKEND = 'project.local.ses_backend.SESBackend'
# AWS_ACCESS_KEY_ID = os.environ.get(
#     "AWS_ACCESS_KEY_ID", default='AKIAIOSFODNN7EXAMPLE')
# AWS_SECRET_ACCESS_KEY = os.environ.get(
#     "AWS_SECRET_ACCESS_KEY", default='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY')
# AWS_SES_REGION = os.environ.get("AWS_SES_REGION", default='ap-south-1')
# AWS_REGION = os.environ.get("AWS_REGION", default='ap-south-1')

# DEFAULT_NOTIFICATION_EMAIL = 'a.suryanarayanan2000@gmail.com'

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',

    # 'aws',
    # 'events',

    'email_service',
    'transactions',
]

# Cors headers
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
]

MIDDLEWARE = [

    # Cors middleware
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'project.local.urls'


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


WSGI_APPLICATION = 'project.local.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("DB_NAME", default='kabootar'),
        'USER': os.environ.get("DB_USER", default='kabootar_user'),
        'PASSWORD': os.environ.get("DB_PASSWORD", default='kabootar_password'),
        'HOST': os.environ.get("DB_HOST", default='database'),
        'PORT': 5432,
        'CONN_MAX_AGE': 600,
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'


USE_I18N = True

USE_TZ = True

# ----------------
# AWS S3 Bucket
# ----------------

# AWS_STORAGE_BUCKET_NAME = os.environ.get(
#     "AWS_S3_BUCKET", default='kabootar')
# AWS_S3_REGION = os.environ.get("AWS_S3_REGION", default='ap-south-1')
# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }

# ----------------
# AWS S3 Bucket Static Files and Media
# ----------------

# AWS_DEFAULT_ACL = 'public-read'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')

# MEDIAFILES_LOCATION = 'media'
# MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'
# DEFAULT_FILE_STORAGE = 'project.local.storage_backend.MediaStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
