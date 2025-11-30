from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-pklu9clsyvbbc0bylcd8c8b=8j5z655@3f0x68a8bz5v_(sd7%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# CORS_ALLOW_ALL_ORIGINS = True   ,跨域相关设置
CORS_ALLOWED_ORIGINS = ['http://localhost:5173']
# ✅ 允许携带 cookie
CORS_ALLOW_CREDENTIALS = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'chat', # 对话管理
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'agents',
    'graph',
    'workspace',
    'user_management',  # 新增用户管理应用
    'channels',
    'rag_service',
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

ROOT_URLCONF = 'HelloWorld.urls'

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

WSGI_APPLICATION = 'HelloWorld.wsgi.application'
# ASGI_APPLICATION = 'HelloWorld.asgi.application' 

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.mysql',   # 使用 MySQL
        'NAME': 'demo_db',                      # 你的数据库名
        'USER': 'demo_user',                    # 数据库用户名
        'PASSWORD': 'demo_pass_123',            # 数据库密码
        'HOST': 'localhost',                    # 本地就用这个
        'PORT': '3306',                         # MySQL 默认端口
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://:redis123456@127.0.0.1:6379/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
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
    'EXCEPTION_HANDLER': 'api.common.handlers.custom_exception_handler',
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
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
}


# Redis 作为 Celery broker（中间件）
CELERY_BROKER_URL = "redis://:redis123456@localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://:redis123456@localhost:6379/1"

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": ["redis://:redis123456@localhost:6379/0"],
        },
    },
}