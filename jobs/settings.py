"""
Django settings for jobs project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
import stripe

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["owatonnajobsonline.com", "www.owatonnajobsonline.com"]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'endless_pagination',
    'account',
    'board',
    'email_user',
    'tinymce',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'jobs.urls'

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

# Used for Django Endless Pagination
TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)

WSGI_APPLICATION = 'jobs.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'board/static'),
)

# Static file serving (heroku)
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR + '/media/')

# Tags that are allowed in the posts
ALLOWED_TAGS = ('p', 'strong', 'ol', 'ul', 'li', 'br', 'em', 'h4', 'h5', 'h6')

# Settings up a user that only has an email field - no username
AUTH_USER_MODEL = 'email_user.EmailUser'

TINYMCE_DEFAULT_CONFIG = {
    'theme' : 'advanced',
    'theme_advanced_blockformats': 'p,h4,h5,h6',
    'theme_advanced_buttons1' : 'formatselect,separator,bold,italic,separator,bullist,numlist',
    'theme_advanced_buttons2' : '',
    'theme_advanced_buttons3' : '',
    'theme_advanced_toolbar_location' : 'top',
    'theme_advanced_toolbar_align': 'left',
    'paste_text_sticky': True,
    'paste_text_sticky_default' : True,
    'plugins': 'paste',
    'paste_auto_cleanup_on_paste' : True,
    'paste_remove_styles': True,
    'paste_remove_styles_if_webkit': True,
    'paste_strip_class_attributes': True,
}

LOGIN_URL = 'login'

# Logging settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },

    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'jobs.log',
            'formatter': 'verbose'
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },

    'loggers': {
        'django': {
            'handlers':['file', 'console'],
            'propagate': True,
            'level':'ERROR',
        },
        'board': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'account': {
            'handlers': ['file'],
            'level': 'DEBUG',
        }
    }
}

ADMINS = [('Ethan', 'ethan@owatonnajobsonline.com'), ]

# Setting to change the look of the site if in pre-launch mode
EMPLOYERS_ONLY = os.environ.get('EMPLOYERS_ONLY') == 'True'

# Stripe settings
stripe.api_key = os.environ.get('API_KEY')
STRIPE_PUSHABLE_KEY = os.environ.get('PUSH_KEY')

# Database settings for Heroku
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES = {'default': dj_database_url.config()}

SECRET_KEY = os.environ.get('SECRET_KEY')

# Use https only
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

os.environ['HTTPS'] = "on"
os.environ['wsgi.url_scheme'] = 'https'

# Email Settings
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = 465
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = 'ethan@owatonnajobsonline.com'

# Import local settings
try:
    from local_settings import *
except ImportError:
    print "Make sure to create local settings"
    pass

# Things that should be in the local settings:
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# SECURITY_KEY = 'jibberish'
#
# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'name',
#        'USER': 'user',
#        'PASSWORD': 'password',
#        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
#        'PORT': '3306',
#    }
# }
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 1025
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_USE_TLS = False
# DEFAULT_FROM_EMAIL = 'testing@example.com'
#
# stripe.api_key = "sk_test_999"
# STRIPE_PUSHABLE_KEY = "pk_test_999"
# STRIPE_ADVANCED_PLAN = "id of plan"
# STRIPE_PREMIUM_PLAN = "id of plan"
