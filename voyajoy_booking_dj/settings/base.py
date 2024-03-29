"""
Django settings for voyajoy_booking_dj project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys
from datetime import timedelta

from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from os.path import dirname

import braintree

BASE_DIR = os.path.join(dirname(dirname(__file__)), '..')

TEMPLATE_DIR = BASE_DIR + '/templates'


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
def _required_env(name):
    try:
        value = os.environ[name]
        if not value:
            raise KeyError
        return value
    except KeyError:
        raise ImproperlyConfigured('Missing env variable: "{}"'.format(name))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bg7^1gdw%d4i+%!e+wvuqpsxx+jn^se0=ldtosxoua$9y2^vll'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'suit',
    'django.contrib.admin',
    'django.contrib.humanize',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'bookingApp',
    'allauth',
    'allauth.account',
    # 'allauth.socialaccount',
    'widget_tweaks',
    'import_export',
    # 'django_twilio',
    'rest_framework',
    # 'endless_pagination',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend"
]

ROOT_URLCONF = 'voyajoy_booking_dj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'bookingApp.context_processors.general_info_context'
            ],
        },
    },
]

WSGI_APPLICATION = 'voyajoy_booking_dj.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# AUTH
SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_FORM_CLASS = 'bookingApp.forms.SignupForm'
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 3
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2
# DEFAULT_FROM_EMAIL = 'no-reply@voyajoy.com'

#
# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'booking.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'bookingApp': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}

# General Infoo
PHONE_NUMBER = '(415) 347-8038'
REFERENCE_KEY = 'VOYAJOYREF#{}'

# TWILIO
TWILIO_ACCOUNT_SID = 'AC64fe41259eca5f10675a01174e5a1147'
TWILIO_AUTH_TOKEN = '9e3a8de6cc68686bb8282e188c053c59'
FROM = '+16502854948'

SUIT_CONFIG = {
    # header
    'ADMIN_NAME': 'Booking Voyajoy ',
    'HEADER_DATE_FORMAT': 'l, j. F Y',
    'HEADER_TIME_FORMAT': 'H:i',

    # forms
    'SHOW_REQUIRED_ASTERISK': True,  # Default True
    'CONFIRM_UNSAVED_CHANGES': True,  # Default True

    'MENU_OPEN_FIRST_CHILD': True,  # Default True
    'MENU_EXCLUDE': ('sites', 'socialaccount', 'auth.group', 'account',),
    # misc
    'LIST_PER_PAGE': 15
}


# Send Grid
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
# SENDGRID_API_KEY = "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"
SENDGRID_API_KEY='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'
DEFAULT_FROM_EMAIL = 'Voyajoy  <no-reply@voyajoy.com>'
