"""
Django settings for kivy_backend project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, BASE_DIR)
sys.path.insert(1, os.path.join(BASE_DIR, 'apps'))  # 设置查找优先级

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$^#f!!t4p3z*m7m90(a0g=wz#2i69_akdzrg=xwpwg^p97#5u5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    "*"
]

CSRF_TRUSTED_ORIGINS = ["https://*", "http://*", "https://122.228.237.118:61929"]
# Application definition

INSTALLED_APPS = [
    # 'jet.dashboard',
    # 'jet',
    # 'grappelli',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    # "daphne",
    'rest_framework',
    'index_page',
    'verification',
    'video_trans',
    'ws4redis'
]
WEBSOCKET_URL = '/ws/'
WS4REDIS_PREFIX = 'ws'
SESSION_EXPIRE_AT_BROWSER_CLOSE = 31536000
WS4REDIS_EXPIRE = 7200

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kivy_backend.urls'


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
                'django.template.context_processors.request',
            ],
            'builtins':['django.templatetags.static']
        },
    },
]
WSGI_APPLICATION = 'kivy_backend.wsgi.application'
ASGI_APPLICATION = 'kivy_backend.asgi.application'  # 添加asgi配置


# 通道层：线上项目最好使用redis数据库
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/0',  # Redis 服务器地址和数据库编号
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',  # Redis 客户端类
        }
    }
}

# 使用 Redis 作为会话引擎（可选）
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': 'utils/dbs/my.cnf',
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False # 这个必须为false，不然渲染上去的时间就不对了。


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = '/media/'   #你上传的文件和图片会默认存在/uploads/editor下

AUTH_USER_MODEL = 'index_page.User'  # 指定替换的用户模型类

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),  # 用于存放静态文件
# ]

if DEBUG:
   STATICFILES_DIRS = [
   os.path.join(BASE_DIR, 'static'),
   ]
else:
   STATIC_ROOT = os.path.join(BASE_DIR,'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# FASTAPI_URL = "http://127.0.0.1:9999"
FASTAPI_URL = "https://122.228.237.118:55617"