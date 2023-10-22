"""
Django settings for clothes_shop project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from django.shortcuts import render
from pathlib import Path
import os
from system.constant import *

# Custom 404 page handler
def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)
# Configure handler404
handler404 = 'webblog.settings.page_not_found_view'
# Custom 500 page handler
def server_error_view(request, exception):
    return render(request, '500.html', status=500)
# Configure handler500
handler500 = 'webblog.settings.server_error_view'


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-s0^^z9b0&#2*%8@8oo05l%52r70gwxn==a-q21#7y9jk0%@b@@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # bs
    'bootstrap5',
    'widget_tweaks',
    # app
    'accounts',
    'cart',
    'core',
    'products',
    'order',
    'test',

    # allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
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

    #custom middleware
    'accounts.custom_middleware.ValidatedCheckMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware', 
]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

ROOT_URLCONF = 'clothes_shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # os.path.join(BASE_DIR,'templates')
            BASE_DIR / 'templates',
            BASE_DIR / 'templates/errors',
            BASE_DIR / 'templates/layouts'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.layout_data',  #use in layout,
                #use for fb login
                'social_django.context_processors.backends', # added
                'social_django.context_processors.login_redirect', # added
            ],
        },
    },
]

WSGI_APPLICATION = 'clothes_shop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dj_deobelly',
        'HOST':'127.0.0.1',
        'USER':'root',
        'PASSWORD':'',
        'PORT':'3306'
    }
}

#Auth custom user model:
AUTH_USER_MODEL = 'accounts.User'

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

LANGUAGE_CODE = 'vi-vn'

TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_I18N = True

USE_TZ = False

#upload file
MEDIA_URL = '/images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',  # Adjust the desired log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
#             'class': 'logging.FileHandler',
#             'filename': 'debug.log',  # File name and location
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',  # Adjust the desired log level
#             'propagate': True,
#         },
#     },
# }

#Login/Logout
LOGOUT_REDIRECT_URL = 'home'
LOGIN_REDIRECT_URL = 'validate_infor_user'
LOGIN_URL = 'login'

SITE_ID = 3

SOCIALACCOUNT_LOGIN_ON_GET=True

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'social_core.backends.facebook.FacebookOAuth2'
    ]

# FACEBOOK_APP_ID = '230793572917126'
# FACEBOOK_APP_SECRET = 'e4770800195704a836e95ba6ff58ec3d'
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'picture',
        ],
        'VERSION': 'v11.0',
    }
}

SOCIAL_AUTH_FACEBOOK_KEY = '230793572917126'
SOCIAL_AUTH_FACEBOOK_SECRET = 'e4770800195704a836e95ba6ff58ec3d'
# SOCIAL_AUTH_FACEBOOK_REDIRECT_URI = 'https://specially-cosmic-donkey.ngrok-free.app/'
SOCIAL_AUTH_FACEBOOK_REDIRECT_URI = 'home'


# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Mail Congigure
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  # Typically, this is 587 for TLS or 465 for SSL
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = SENDER_MAIL
EMAIL_HOST_PASSWORD = 'pzigjrvkvaxupehr'

# Django don  not think it is being served via https 
# because it's behind a reverse proxy, you need to configure it. 
# See this answer https://stackoverflow.com/a/65934202/548562
# needed for login with fb
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_COOKIE_SECURE = True