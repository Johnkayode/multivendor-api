import os

from datetime import timedelta
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = os.getenv('SECRET_KEY')
        

DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS')




AUTH_USER_MODEL = "vendor.CustomUser"

REST_FRAMEWORK = {

    'DEFAULT_PERMISSION_CLASSES': [
         'rest_framework.permissions.AllowAny',
        ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
     'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
     )
}


JWT_AUTH = {
  'JWT_ENCODE_HANDLER':
  'rest_framework_jwt.utils.jwt_encode_handler',
  'JWT_DECODE_HANDLER':
  'rest_framework_jwt.utils.jwt_decode_handler',
  'JWT_PAYLOAD_HANDLER':
  'rest_framework_jwt.utils.jwt_payload_handler',
  'JWT_PAYLOAD_GET_USER_ID_HANDLER':
  'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
  'JWT_RESPONSE_PAYLOAD_HANDLER':
  'rest_framework_jwt.utils.jwt_response_payload_handler',
 
  'JWT_SECRET_KEY': os.getenv('JWT_SECRET_KEY'),
  'JWT_GET_USER_SECRET_KEY': None,
  'JWT_PUBLIC_KEY': None,
  'JWT_PRIVATE_KEY': None,
  'JWT_ALGORITHM': 'HS256',
  'JWT_VERIFY': True,
  'JWT_VERIFY_EXPIRATION': True,
  'JWT_LEEWAY': 0,
  'JWT_EXPIRATION_DELTA': timedelta(days=30),
  'JWT_AUDIENCE': None,
  'JWT_ISSUER': None,
  'JWT_ALLOW_REFRESH': False,
  'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=30),
  'JWT_AUTH_HEADER_PREFIX': 'Bearer',
  'JWT_AUTH_COOKIE': None,
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "rest_framework",
    "vendor",
    "customer",
    "administrator",
    "order",
    "product",
    "wallet"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'multivendor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'multivendor.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'site.sqlite3',
    }
}


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

BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Lagos'

EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER=os.getenv('EMAIL_HOST_USER')
EMAIL_USE_TLS=os.getenv('EMAIL_USE-TLS')
EMAIL_PORT=os.getenv('EMAIL_PORT')
EMAIL_HOST=os.getenv('EMAIL_HOST')

 

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = True



STATIC_URL = '/static/'

MEDIA_URL = '/media/'



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
