from pathlib import Path
from datetime import timedelta
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "unsafe-secret-key-for-dev")  # 默认值仅用于开发

DEBUG = os.environ.get("DJANGO_DEBUG", "0") == "1"

# CORS_ALLOW_ALL_ORIGINS = True   ,跨域相关设置
CORS_ALLOWED_ORIGINS = ['http://localhost:5173']
# ✅ 允许携带 cookie
CORS_ALLOW_CREDENTIALS = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "0.0.0.0"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'agents',
    'graph',
    'workspace',
    'user_management',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_DATABASE'),
        'USER': os.environ.get('MYSQL_USER'),
        'PASSWORD': os.environ.get('MYSQL_ROOT_PASSWORD'),
        'HOST': os.environ.get('MYSQL_HOST'),
        'PORT': '3306',
        'OPTIONS': {
            'auth_plugin': 'mysql_native_password',
            'ssl': {'ssl_disabled': True}, 
        },
    }
}

REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0",
        'OPTIONS': {'CLIENT_CLASS': 'django_redis.client.DefaultClient'}
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'  # 中国时区 (UTC+8)
# TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Media files (uploaded by users)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 设置认证类
'''
这是 全局默认认证类。
意思是 所有 DRF 的 APIView / @api_view 的视图，
如果你没有显式指定 @authentication_classes，都会用这个类去验证用户。
'''
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER':'api.common.handlers.custom_exception_handler', #'EXCEPTION_HANDLER': None ,'EXCEPTION_HANDLER':'api.common.handlers.custom_exception_handler',
    # 使用自定义认证类：优先从 Authorization header，再从 Cookie('access') 获取 JWT
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'user_management.authentication.CookieOrHeaderJWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'user_management.authentication.IsCustomAuthenticated',
    ),
}

# Simple JWT settings (can be overridden in environment-specific settings)
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
}

