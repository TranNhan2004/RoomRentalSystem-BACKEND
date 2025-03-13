import os

from dotenv import load_dotenv
from pathlib import Path
from datetime import timedelta

load_dotenv('.env.development')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split()
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS').split()
CORS_TRUSTED_ORIGINS = os.getenv('CORS_TRUSTED_ORIGINS').split()
CORS_ORIGINS_WHITELIST = os.getenv('CORS_ORIGINS_WHITELIST').split()

# SESSION_COOKIE_DOMAIN = "localhost"
# CSRF_COOKIE_DOMAIN = "localhost"

AUTH_USER_MODEL = 'user_account_app_label.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ]
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
BACKEND_URL_FOR_SEND_EMAIL = os.getenv('BACKEND_URL_FOR_SEND_EMAIL')
FRONTEND_URLS_FOR_SEND_EMAIL = {
    'MANAGER': os.getenv('MANAGER_FRONTEND_URL_FOR_SEND_EMAIL'),
    'LESSOR': os.getenv('LESSOR_FRONTEND_URL_FOR_SEND_EMAIL'),
    'RENTER': os.getenv('RENTER_FRONTEND_URL_FOR_SEND_EMAIL')
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15, seconds=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=3, hours=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id'
}

SESSION_REFRESH_TOKEN_COOKIE_KEYS = {
    'MANAGER': os.getenv('SESSION_MANAGER_REFRESH_TOKEN_COOKIE_KEY'),
    'LESSOR': os.getenv('SESSION_LESSOR_REFRESH_TOKEN_COOKIE_KEY'),
    'RENTER': os.getenv('SESSION_RENTER_REFRESH_TOKEN_COOKIE_KEY')
}
SESSION_REFRESH_TOKEN_COOKIE_MAX_AGE = int(os.getenv('SESSION_REFRESH_TOKEN_COOKIE_MAX_AGE'))
SESSION_REFRESH_TOKEN_COOKIE_DOMAIN = os.getenv('SESSION_REFRESH_TOKEN_COOKIE_DOMAIN')
SESSION_REFRESH_TOKEN_COOKIE_PATH = os.getenv('SESSION_REFRESH_TOKEN_COOKIE_PATH')

GOONG_API_KEY = os.getenv('GOONG_API_KEY')

MAX_SEARCH_ROOM_HISTORY_COUNT = int(os.getenv('MAX_SEARCH_ROOM_HISTORY_COUNT'))

RECOMMENDATION_ROOM_CHARGE_SCALE_RATE = float(os.getenv('RECOMMENDATION_ROOM_CHARGE_SCALE_RATE'))
RECOMMENDATION_ELECTRICITY_CHARGE_SCALE_RATE = float(os.getenv('RECOMMENDATION_ELECTRICITY_CHARGE_SCALE_RATE'))
RECOMMENDATION_WATER_CHARGE_SCALE_RATE = float(os.getenv('RECOMMENDATION_WATER_CHARGE_SCALE_RATE'))
RECOMMENDATION_WIFI_CHARGE_SCALE_RATE = float(os.getenv('RECOMMENDATION_WIFI_CHARGE_SCALE_RATE'))
RECOMMENDATION_RUBBISH_CHARGE_SCALE_RATE = float(os.getenv('RECOMMENDATION_RUBBISH_CHARGE_SCALE_RATE'))
RECOMMENDATION_DISTANCE_VALUE_SCALE_RATE = float(os.getenv('RECOMMENDATION_DISTANCE_VALUE_SCALE_RATE'))
RECOMMENDATION_K_CLOSEST_ROOMS = int(os.getenv('RECOMMENDATION_K_CLOSEST_ROOMS'))
RECOMMENDATION_CHOOSE_ROOM_RATE = float(os.getenv('RECOMMENDATION_CHOOSE_ROOM_RATE'))

# Application definition
INSTALLED_APPS = [
    'corsheaders',
    
    'apps.address',
    'apps.user_account',
    'apps.rental_room',
    'apps.distance',
    'apps.review',
    'apps.save_for_later',
    'apps.search_room_history',
    'apps.recommendation',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    'rest_framework_simplejwt',

    'django_filters',
    'django_cleanup',
    'sslserver',
]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend_project.urls'

# settings.py

# Template settings
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
            ],
        },
    },
]

WSGI_APPLICATION = 'backend_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': int(os.getenv('DB_PORT')),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'apps.user_account.validators.CustomPasswordValidator',
    }
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/media/' 
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'