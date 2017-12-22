"""
Django settings for overfiftyfive project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import environ

'''
django-environ
https://github.com/joke2k/django-environ
'''
root = environ.Path(__file__) - 3 # three folder back (/a/b/c/ - 3 = /)
env = environ.Env(DEBUG=(bool, False),) # set default values and casting
environ.Env.read_env() # reading .env file

SITE_ROOT = root()


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY') # Raises ImproperlyConfigured exception if SECRET_KEY not in os.environ

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG') # False if not in os.environ

ALLOWED_HOSTS = ['*']

SITE_ID = 1


# Application definition

# This configuration ensures that all authenticated users from the public
# schema to exist authenticated in the tenant schemas as well. This is
# important to have "django-tenants" work
SESSION_COOKIE_DOMAIN = '.' + env("O55_APP_HTTP_DOMAIN")


SHARED_APPS = (
    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Extra Django Apps
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.postgres',   # Postgres full-text search: https://docs.djangoproject.com/en/1.10/ref/contrib/postgres/search/
    'django.contrib.gis',        # Geo-Django https://docs.djangoproject.com/en/dev/ref/contrib/gis/

    # Third Party Apps
    'django_tenants',  # (mandatory)
    'trapdoor',
    # . . .

     # Shared Apps
    'shared_home',
    'shared_foundation'
    # . . .
)

TENANT_APPS = (
    # The following Django contrib apps must be in TENANT_APPS
    'django.contrib.contenttypes',

    # Tenant-specific apps
    # . . .
)

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]


MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',       # Third Party
    'corsheaders.middleware.CorsMiddleware',                     # Third Party
    'trapdoor.middleware.TrapdoorMiddleware',                    # Third Party
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',              # Extra Django App
    'htmlmin.middleware.HtmlMinifyMiddleware',                # Third Party
    'htmlmin.middleware.MarkRequestMiddleware',               # Third Party
]

ROOT_URLCONF = 'overfiftyfive.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'shared_foundation.context_processors.foundation_constants', # Custom App
            ],
        },
    },
]

WSGI_APPLICATION = 'overfiftyfive.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

###########################################
#TODO: WE WANT TO MAKE IT LOOK LIKE THIS. #
###########################################
# DATABASES = {
#     'default': env.db(), # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
#     # 'default': {
#     #     'ENGINE': 'django.db.backends.sqlite3',
#     #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     # }
# }

DATABASES = {
    "default": {
        'CONN_MAX_AGE': 0,
        'ENGINE': 'django_tenants.postgresql_backend',
        "NAME": env("DB_NAME", default="overfiftyfive_db"),
        "USER": env("DB_USER", default="django"),
        "PASSWORD": env("DB_PASSWORD", default="123password"), # YOU MUST CHANGE IN PROD!
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env("DB_PORT", default="5432"),
    }
}

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

ORIGINAL_BACKEND = "django.contrib.gis.db.backends.postgis"

TENANT_MODEL = "shared_foundation.SharedFranchise"

TENANT_DOMAIN_MODEL = "shared_foundation.SharedFranchiseDomain"


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

ugettext = lambda s: s
LANGUAGES = (
    ('en', ugettext('English')),
#    ('fr', ugettext('French')),
#    ('es', ugettext('Spanish')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)


# Email
# https://docs.djangoproject.com/en/1.11/topics/email/

EMAIL_BACKEND = env("EMAIL_BACKEND")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
DEFAULT_TO_EMAIL = env("DEFAULT_TO_EMAIL")


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


# django-cors-headers
# https://github.com/ottoyiu/django-cors-headers

CORS_ORIGIN_ALLOW_ALL=True


# django-htmlmin
# https://github.com/cobrateam/django-htmlmin

HTML_MINIFY = env("HTML_MINIFY")
KEEP_COMMENTS_ON_MINIFYING = env("KEEP_COMMENTS_ON_MINIFYING")


########
# TODO #
########
# # Anymail
# #  https://github.com/anymail/django-anymail
#
# ANYMAIL = {
#     # (exact settings here depend on your ESP...)
#     "MAILGUN_API_KEY": env("MAILGUN_ACCESS_KEY"),
#     "MAILGUN_SENDER_DOMAIN": env("MAILGUN_SERVER_NAME"),
# }

########
# TODO #
########
# # Error Emailing
# # https://docs.djangoproject.com/en/dev/topics/logging/
#
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler',
#             'include_html': False, # Set to this value to prevent spam
#         }
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
#         },
#         'django.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#     },
# }


# Application Specific Variables #
#

# Variables define what URL structure to use in our system.
O55_APP_HTTP_PROTOCOL = env("O55_APP_HTTP_PROTOCOL")
O55_APP_HTTP_DOMAIN = env("O55_APP_HTTP_DOMAIN")
