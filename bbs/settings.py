"""
Django settings for bbs project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from urllib.parse import urlencode

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o$$uonv4r#!-8$st#lauz3t8&o*_(^f(&%_u*wqqrc1v1lk#c_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'post',
    'user',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',         # |  process_request   process_response  ^
    'django.contrib.sessions.middleware.SessionMiddleware',  # |  process_request   process_response  |
    'django.middleware.common.CommonMiddleware',             # |  process_request   process_response  |
    'django.middleware.csrf.CsrfViewMiddleware',             # V  process_request   process_response  |
    # 'common.middleware.simple_middleware'
    # 'common.middleware.BlockSpiderMiddleware',
]

ROOT_URLCONF = 'bbs.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'bbs.wsgi.application'

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# Cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PICKLE_VERSION": -1,
        }
    }
}


REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 3
}


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
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

STATIC_URL = '/statics/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "statics"),
]

MEDIA_ROOT = 'medias'
MEDIA_URL = '/medias/'


# WeiBo OAuth
WB_APP_KEY = '1310374555'
WB_APP_SECRET = 'e5cf3ddc50d77ba6f038013003c29550'
WB_CALLBACK = 'http://bbs.seamile.org/weibo/callback/'

# auth api
WB_AUTH_API = 'https://api.weibo.com/oauth2/authorize'
WB_AUTH_ARGS = {
    'client_id': WB_APP_KEY,
    'redirect_uri': WB_CALLBACK,
    'response_type': 'code',
}
WB_AUTH_URL = '%s?%s' % (WB_AUTH_API, urlencode(WB_AUTH_ARGS))  # 引导用户完成授权的页面

# access token api
WB_ACCESS_TOKEN_API = 'https://api.weibo.com/oauth2/access_token'
WB_ACCESS_TOKEN_ARGS = {
    'client_id': WB_APP_KEY,
    'client_secret': WB_APP_SECRET,
    'redirect_uri': WB_CALLBACK,
    'grant_type': 'authorization_code',
    'code': None,
}

# users show api
WB_USER_SHOW_API = 'https://api.weibo.com/2/users/show.json'
WB_USER_SHOW_ARGS = {
    'access_token': None,
    'uid': None,
}
