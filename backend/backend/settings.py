import configparser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# 读取配置文件
config = configparser.ConfigParser()
config.read(BASE_DIR / 'config.ini', encoding='utf-8')

SECRET_KEY = "django-insecure-n)ww$(hm%#sa%p=q4$^%$237mikv8vj4-r6%mt+93!(o=$*ffn"

DEBUG = True

SECURE_SSL_REDIRECT = False

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'authority.apps.AuthorityConfig',
    'article.apps.ArticlesConfig',
    'categorie.apps.CategoriesConfig',
    'comment.apps.CommentsConfig',
    'media.apps.MediaConfig',
    'user.apps.UsersConfig',
    'ai.apps.AiConfig',
    'sslserver'
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "backend.middleware.RequestLoggingMiddleware",
]

AUTHENTICATION_BACKENDS = [
    'user.utils.MultiFieldAuthBackend',
    'django.contrib.auth.backends.ModelBackend'
]

CORS_ALLOWED_ORIGINS = [
    "http://codejourney.cn",
    "http://localhost:5173"
]

ALLOWED_HOSTS = [
    "codejourney.cn",
    "localhost",
    "127.0.0.1"
]

CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "backend.wsgi.application"

# 数据库配置（从 config.ini 读取）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config.get('database', 'name'),
        'HOST': config.get('database', 'host'),
        'PORT': config.getint('database', 'port'),
        'USER': config.get('database', 'user'),
        'PASSWORD': config.get('database', 'password')
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt.authentication.JWTAuthentication'],
}

from datetime import timedelta
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "userId",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

AUTH_USER_MODEL = 'user.User'

LANGUAGE_CODE = "en-us"
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs" / "api.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "api": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


# =============================================
# 从 config.ini 读取的密钥配置
# =============================================
CRYPTOJS_KEY = config.get('keys', 'cryptojs_key')

# =============================================
# 从 config.ini 读取的邮箱配置
# =============================================
EMAIL_HOST_USER = config.get('email', 'host_user')
EMAIL_HOST_PASSWORD = config.get('email', 'host_password')
SMTP_SERVER = config.get('email', 'smtp_server')
SMTP_PORT = config.getint('email', 'smtp_port')

# =============================================
# 从 config.ini 读取的七牛云配置
# =============================================
QINIU_ACCESS_KEY = config.get('qiniu', 'access_key')
QINIU_SECRET_KEY = config.get('qiniu', 'secret_key')
QINIU_BUCKET_NAME = 'sunboy-store'
QINIU_DOMAIN_URL = 'https://niu.codejourney.cn'
QINIU_MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# =============================================
# 从 config.ini 读取的 Redis 配置
# =============================================
REDIS_HOST = config.get('redis', 'host')
REDIS_PORT = config.getint('redis', 'port')
REDIS_DB = config.getint('redis', 'db')
REDIS_PASSWORD = config.get('redis', 'password')

# =============================================
# 从 config.ini 读取的 MiniMax AI 配置
# =============================================
MINIMAX_API_KEY = config.get('minimax', 'api_key')
MINIMAX_BASE_URL = config.get('minimax', 'base_url')
MINIMAX_MODEL = config.get('minimax', 'model')