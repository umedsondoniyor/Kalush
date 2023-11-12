from pathlib import Path
import os
from pathlib import Path
import posixpath

from django.conf import global_settings
from django.conf.locale import LANG_INFO
import dotenv
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-5%ldndskwkso2+-7m&%+_jhm-ito@#h#p!j76#@$)92o#k!2dt'
# security
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)
SECRET_KEY = os.getenv('SECRET_KEY')
# end security
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Allauth
SITE_ID = 1
# allauth
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'modeltranslation',
    'jazzmin',
    'django.contrib.admin',
    # custom
    'mainhome',
    'Product',
    "Product.templatetags",
    'Profile',
    'Cart',
    # allauth apps
    # Required allauth apps:
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'storages',  # for AWS
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'Kalush.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'Kalush.context_processors.default',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Kalush.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

LANGUAGES = [
    ('tg', _('Tajik')),
    ('en', _('English')),
    ('ru', _('Russian')),
]

EXTRA_LANG_INFO = {
    'tg': {
        'bidi': False,
        'code': 'tg',
        'name': 'Tajik',
        'name_local': u'Тоҷикӣ',
    },
}

LANG_INFO = dict(list(LANG_INFO.items()) + list(EXTRA_LANG_INFO.items()))
LANG_INFO = LANG_INFO

global_settings.LANGUAGES = global_settings.LANGUAGES + [("tg", 'Tajik')]

LOCALE_PATHS = [
    BASE_DIR/'locale/',
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_LANGUAGES = ('en', 'ru', 'tg')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATIC_URL = 'static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# URL to use when referring to static files located in STATIC_ROOT.
STATIC_URL = '/static/'

# The absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # It's often a good idea to name this 'staticfiles' to avoid confusion with your source static directory, which could be named 'static'.

# The file storage engine to use when collecting static files with the collectstatic management command.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Replace 'your_static_directory' with the path to where you're developing your static files.
]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'moviefymovie@gmail.com'  # Replace with your Gmail email address
EMAIL_HOST_PASSWORD = 'zillkirhiueyflgp'  # Replace with your Gmail password or app-specific password

# AWS

# AWS_ACCESS_KEY_ID = 'AKIASERXPYECKC4ABB6S'
# AWS_SECRET_ACCESS_KEY = 'XaAgOLZ1NLkIjBjmSeVQGldIQJ49J5pRdl7UmcQP'
# AWS_STORAGE_BUCKET_NAME = 'moviefy-django'
# AWS_S3_REGION_NAME = 'eu-central-1'
#
# # Use the S3 storage backend for media files
# # DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# if DEBUG:
#     DEFAULT_FILE_STORAGE = 'Fromkor.storage_backends.MediaStorage'
