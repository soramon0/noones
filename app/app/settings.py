"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

from django.utils.translation import gettext_lazy as _
import environ
from celery.schedules import crontab

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = env('DEBUG')

SECRET_KEY = env('SECRET_KEY')   

# 'DJANGO_ALLOWED_HOSTS' should be a single string of hosts with a space between each.
# For example: 'DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'
ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(' ')

if not DEBUG:
    # Security Headers
    SECURE_HSTS_SECONDS = env('SECURE_HSTS_SECONDS')
    SECURE_SSL_REDIRECT = env('SECURE_SSL_REDIRECT')
    SESSION_COOKIE_SECURE = env('SESSION_COOKIE_SECURE')
    CSRF_COOKIE_SECURE = env('CSRF_COOKIE_SECURE')
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env('SECURE_HSTS_INCLUDE_SUBDOMAINS')
    SECURE_HSTS_PRELOAD = env('SECURE_HSTS_PRELOAD')
    # Setting up sentry in production
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn="https://dc97e9d7dd944c8896c85471fdde5892@o526360.ingest.sentry.io/5641807",
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "accounts.apps.AccountsConfig",
    "models.apps.ModelsConfig",
    "updates.apps.UpdatesConfig",
    "pages",
    "core",
    "theme",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

INTERNAL_IPS = []

if DEBUG:
    INSTALLED_APPS.append("django_seed")

    # use debug toolbar in dev mode
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS.append('127.0.0.1')


ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "theme/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    "default": env.db(),
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Testing config
TEST_RUNNER = 'app.runner.TestRunner'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "fr"
# Provide a lists of languages which the site supports.
LANGUAGES = (("en", _("English")), ("fr", _("French")))

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

APPEND_SLASH = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = "/static/"

# Custom User
AUTH_USER_MODEL = "core.User"

# settting up Logging
CONSOLE_LOGGING_FORMAT = '{levelname}: {asctime} {module} {process:d} {thread:d} {pathname} {funcName} {lineno} {name}: {message}'
CONSOLE_LOGGING_FILE = os.path.join(BASE_DIR, 'temp/django-wrds.log')
CONSOLE_QUERY_LOGGING_FILE = os.path.join(BASE_DIR, 'temp/django-queries.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': CONSOLE_LOGGING_FORMAT,
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': CONSOLE_LOGGING_FILE,
            'mode': 'a',
            'encoding': 'utf-8',
            'formatter': 'verbose',
            'backupCount': 5,
            'maxBytes': 10485760,
        },
        'query_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': CONSOLE_QUERY_LOGGING_FILE,
            'mode': 'a',
            'encoding': 'utf-8',
            'backupCount': 5,
            'maxBytes': 10485760,
        },
    },
    'loggers': {
        'root': {
            'handlers': ['console', 'mail_admins', 'file'],
            'level': env('ROOT_LOG_LEVEL')
        },
        'django': {
            'handlers': ['console', 'mail_admins', 'file'],
            'level': env('DJANGO_LOG_LEVEL'),
            'propagte': False
        },
        'django.server': {
            'propagte': True
        },
        'django.db.backends': {
            'propagte': False,
            'level': 'DEBUG',
            'handlers': ['query_file']
        }
    }
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "app/static")]

# Media Folder Settings
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# EMAIL CONFIG
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, "temp/emails")
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True

# REST FRAMEWORK CONFIG
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 20,
    "MAX_LIMIT": 20,
}

# CELERY CONFIG
CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = 'UTC'
CELERY_BEAT_SCHEDULE = {
    'context': {
        'task': 'updates.delete_updates',
        'schedule': crontab(minute=0, hour=0)  # Execute daily at midnight.
    }
}
