import datetime
import os

import dj_database_url
from prettyconf import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECRET KEY
# ------------------------------------------------------------------------------
# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = config('SECRET_KEY')

# DEBUG
# ------------------------------------------------------------------------------
# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = config('DEBUG', default=False, cast=config.boolean)

# ALLOWED_HOSTS
# ------------------------------------------------------------------------------

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=['*',], cast=config.list)

# AUTH
# ------------------------------------------------------------------------------

AUTH_USER_MODEL = 'accounts.User'

# APP CONFIGURATION
# ------------------------------------------------------------------------------

DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
]

LOCAL_APPS = [
    'core',
    'accounts',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/1.10/topics/http/middleware/

SECURITY_MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
]

DJANGO_MIDDLEWARES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

THIRD_PARTY_MIDDLEWARES = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

MIDDLEWARE = SECURITY_MIDDLEWARE + THIRD_PARTY_MIDDLEWARES + DJANGO_MIDDLEWARES

# AUTHENTICATION BACKENDS
# ------------------------------------------------------------------------------

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.AllowAllUsersModelBackend'
]

# URL Configuration
# ------------------------------------------------------------------------------

ROOT_URLCONF = 'api.urls'

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'public/'),
        ],
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

# WGSI CONFIGURATION
# ------------------------------------------------------------------------------

WSGI_APPLICATION = 'api.wsgi.application'

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASE_URL = config('DATABASE_URL')

DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL, conn_max_age=30)
}

# CACHE CONFIGURATION
# ------------------------------------------------------------------------------

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_URL'),
    }
}

# SESSION ENGINE
# ------------------------------------------------------------------------------

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# PASSWORD VALIDATION
# ------------------------------------------------------------------------------
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

# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
SITE_ID = 1

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'assets/')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'public/static/'),
]

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/1.10/ref/settings/#media-root
# https://docs.djangoproject.com/en/1.10/ref/settings/#media-url

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/'),

# Django REST framework
# ------------------------------------------------------------------------------
# http://www.django-rest-framework.org/

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter'
    ),
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.ScopedRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '20/minute',
        'user': '120/minute',
        'health-check': '12/minute',
    },
    'EXCEPTION_HANDLER': 'core.exceptions.exception_handler',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'PAGE_SIZE': 50
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(minutes=15),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(hours=4),
}


# Djoser
# ------------------------------------------------------------------------------

DJOSER = {
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': not DEBUG,
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': True,
    'SET_PASSWORD_RETYPE': True,
    'SERIALIZERS': {
        'user': 'accounts.serializers.UserSerializer'
    }
}

# Email
# ------------------------------------------------------------------------------

EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST_USER = config('EMAIL_HOST', default=None)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default=None)
EMAIL_HOST = config('EMAIL_BACKEND', default=None)
EMAIL_PORT = config('EMAIL_PORT', default=587)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=config.boolean)

# LOGGING
# ------------------------------------------------------------------------------

LOG_LEVEL = config('LOG_LEVEL', default='INFO').upper()
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        'django': {
            'level': LOG_LEVEL,
            'handlers': ['console'],
        },
        'django.backends.db': {
            'level': LOG_LEVEL,
            'handlers': ['console'],
        },
        'gunicorn': {
            'level': LOG_LEVEL,
            'handlers': ['console'],
        },
    }
}
