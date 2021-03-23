# cridad/settings.py


import os
import django_heroku
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY=os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['cridadshop.herokuapp.com', 'www.cridad.com', 'cridad.com']


# Application definition

INSTALLED_APPS = [
    'register',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'shop',
    'storages',
    "paystack.frameworks.django",
    
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

ROOT_URLCONF = 'cridad.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            "libraries": {
                "paystack": "paystack.frameworks.django.templatetags.paystack"
            },
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cridad.wsgi.application'



#Email for forget password
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # during development only

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "cridadgh@gmail.com"
EMAIL_HOST_PASSWORD = os.environ.get("CRIDAD_EMAIL_PASSWORD")

#DEFAULT_FROM_EMAIL = 'Cridad Support Team <noreply@example.com>'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_REDIRECT_URL = "shop:shop"
LOGIN_URL = "/login"
LOGOUT_REDIRECT_URL = "/login"

#Paystack Credentials
#TEST
#PAYSTACK_PUBLIC_KEY = 'pk_test_00a92d9e8ddfe626689a1afcfe7e7a92d7d94cca'
#PAYSTACK_SECRET_KEY = 'sk_test_179bba0a1060ab30c807e53ebd1c0ee3c99756de'

#LIVE KEYS
#===============================================================
PAYSTACK_PUBLIC_KEY = os.environ.get('CRIDAD_PAYSTACK_PUBLIC_KEY') 
PAYSTACK_SECRET_KEY = os.environ.get('CRIDAD_PAYSTACK_SECRET_KEY') 

PAYSTACK_FAILED_URL = "shop:checkout"
PAYSTACK_SUCCESS_URL ="shop:shop"

#=====================================================================

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIR = os.path.join(BASE_DIR, 'static')


# Crispy forms for modifying our login and logout pages
CRISPY_TEMPLATE_PACK = "bootstrap4"

# MEDIA responsible for pictures
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#MEDIA_URL = '/media/'
MEDIA_URL = '//%s.s3.amazonaws.com/media/cridad-bucket/'


django_heroku.settings(locals())


db_from_env=dj_database_url.config(conn_max_age=600)
DATABASES["default"].update(db_from_env)


AWS_SECRET_ACCESS_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_ACCESS_KEY_ID=os.environ.get('AWS_ACCESS_KEY_ID')
AWS_STORAGE_BUCKET_NAME=os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME=os.environ.get('AWS_S3_REGION_NAME')
AWS_S3_SIGNATURE_VERSION='s3v4'
AWS_S3_FILE_OVERWRITE=False
AWS_DEFAULT_ACL=None
DEFAULT_FILE_STORAGE='storages.backends.s3boto3.S3Boto3Storage'

