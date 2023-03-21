"""
Django settings for tgctm project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", True)

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1").split(" ")
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "http://127.0.0.1").split(" ")


# Application definition

INSTALLED_APPS = [
    'ctm.apps.CtmConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5',
    'social_django',
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

AUTHENTICATION_BACKENDS = (
    'social_core.backends.keycloak.KeycloakOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'tgctm.urls'

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

WSGI_APPLICATION = 'tgctm.wsgi.application'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("MYSQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("MYSQL_DATABASE", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("MYSQL_USER", "user"),
        "PASSWORD": os.environ.get("MYSQL_PASSWORD", "password"),
        "HOST": os.environ.get("MYSQL_HOST", "localhost"),
        "PORT": os.environ.get("MYSQL_PORT", "5432"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.environ.get("STATIC_ROOT", "./static_built")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


## TGBT IDAM Settings

IDAM_API_URL=os.environ.get("TGBT_IDAM_API_URL", "https://tgbt-idam.gathering.org/")
IDAM_API_KEY=os.environ.get("TGBT_IDAM_API_KEY")

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Add you connection settings here
SOCIAL_AUTH_KEYCLOAK_KEY = os.environ.get("SOCIAL_AUTH_KEYCLOAK_KEY")
SOCIAL_AUTH_KEYCLOAK_SECRET = os.environ.get("SOCIAL_AUTH_KEYCLOAK_SECRET")
SOCIAL_AUTH_KEYCLOAK_PUBLIC_KEY = os.environ.get("SOCIAL_AUTH_KEYCLOAK_PUBLIC_KEY")
SOCIAL_AUTH_KEYCLOAK_AUTHORIZATION_URL = os.environ.get("SOCIAL_AUTH_KEYCLOAK_AUTHORIZATION_URL")
SOCIAL_AUTH_KEYCLOAK_ACCESS_TOKEN_URL = os.environ.get("SOCIAL_AUTH_KEYCLOAK_ACCESS_TOKEN_URL")
SOCIAL_AUTH_KEYCLOAK_ID_KEY = os.environ.get("SOCIAL_AUTH_KEYCLOAK_ID_KEY")
SOCIAL_AUTH_KEYCLOAK_LOGOUT_URL = os.environ.get("SOCIAL_AUTH_KEYCLOAK_LOGOUT_URL")
SOCIAL_AUTH_KEYCLOAK_EXTRA_DATA=[("refresh_token","refresh_token")]

SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

LOGIN_REDIRECT_URL = '/'