"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from os.path import join
from dotenv import load_dotenv
from google.oauth2 import service_account
import json

PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))
if os.getenv('ENV') == 'local':
    dotenv_path = join(PROJECT_PATH, '../config/backend/.env.local')
else:
    dotenv_path = join(PROJECT_PATH, '../config/backend/.env')
load_dotenv(dotenv_path)

API_CLIENT_ID = os.getenv('API_CLIENT_ID')
API_CLIENT_SECRET = os.getenv('API_CLIENT_SECRET')
API_REDIRECT_URI = os.getenv('API_REDIRECT_URI')
API_AUTH_URI = 'https://api.intra.42.fr/oauth/authorize?client_id=' + API_CLIENT_ID + '&redirect_uri=' + API_REDIRECT_URI + '&response_type=code'
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
APP_PASSWORD = os.getenv('APP_PASSWORD')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(eg1%h@r8fyk-^i@id)x$a@yv@^d)anwc-bwbwowkz=@z&2rei'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "backend",
    "localhost",
]


# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'ft_user',
	'ft_auth',
	'ft_game',
	'ft_lobby',
	'ft_room',
	# 'ft_onlinestatus',
	'channels',
	'corsheaders',
	'django_otp',
    'django_otp.plugins.otp_totp',
	'django_otp.plugins.otp_email',
	'rest_framework',
	'rest_framework_simplejwt',
    'django_prometheus',
    'storages',
]

ASGI_APPLICATION = 'backend.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
	}
}


CORS_ALLOWED_ORIGINS = [ 'http://localhost:5173' ]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'DELETE',
    'PUT',
    'PATCH',
]

CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
]

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [ 'http://localhost:5173' ]

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}


from datetime import timedelta

SIMPLE_JWT = {
  # It will work instead of the default serializer(TokenObtainPairSerializer).
	"TOKEN_OBTAIN_SERIALIZER": "ft_auth.serializers.MyTokenObtainPairSerializer",
	"ACCESS_TOKEN_LIFETIME": timedelta(minutes=300),
	"REFRESH_TOKEN_LIFETIME": timedelta(days=1),
	"ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": JWT_SECRET_KEY,
    'USER_ID_FIELD': 'uid',
  # ...
}

AUTH_USER_MODEL = 'ft_user.CustomUser'

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'ft_auth.middleware.InsertJWT',
	'ft_auth.middleware.CustomAuthentication',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django_prometheus.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'postgresql',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#load env

# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379/1',
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#             'ASYNC_CLIENT_CLASS': "django_redis.client.AsyncClient", # add async cache
#         }
#     }
# }



DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = os.getenv('GS_BUCKET_NAME')
MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'KeyValueFormatter': {
            'format': '%(asctime)s [%(levelname)s] message=%(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'KeyValueFormatter',
        },
        'django_error_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'log/django_error.log',
            'formatter': 'KeyValueFormatter',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['django_error_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['django_error_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    }
}
SERVICE_ACCOUNT_INFO = {
    "type": os.getenv('TYPE'),
    "project_id": os.getenv('PROJECT_ID'),
    "private_key_id": os.getenv('PRIVATE_KEY_ID'),
    "private_key": os.getenv('PRIVATE_KEY').replace('\\n', '\n'),
    "client_email": os.getenv('CLIENT_EMAIL'),
    "client_id": os.getenv('CLIENT_ID'),
    "auth_uri": os.getenv('AUTH_URI'),
    "token_uri": os.getenv('TOKEN_URI'),
    "auth_provider_x509_cert_url": os.getenv('AUTH_PROVIDER_X509_CERT_URL'),
    "client_x509_cert_url": os.getenv('CLIENT_X509_CERT_URL'),
    "universe_domain": os.getenv('UNIVERSE_DOMAIN'),
}

GS_CREDENTIALS = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO)
