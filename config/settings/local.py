import os
from decouple import config
from django.urls import reverse, reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


SECRET_KEY = config('SECRET_KEY')
# DEBUG = config('DEBUG', default=False, cast=bool)


DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


THIRD_PARTY_APPS = [
    'bootstrap4',

]

PROJECT_APPS = [
    'account.users.apps.UsersConfig',
    'account.apps.AccountConfig',
]


INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'account.middlewares.ActiveUserMiddleware', # custom
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_USER_MODEL = 'users.User'


AUTHENTICATION_BACKENDS = (
'django.contrib.auth.backends.ModelBackend',
'account.authentication.EmailAuthBackend',
'account.authentication.CaseInsensitiveModelBackend',

)

BACKEND_AUTH = 'django.contrib.auth.backends.ModelBackend'


LOGIN_REDIRECT_URL = reverse_lazy('/')
LOGIN_URL = reverse_lazy('account:login')
LOGOUT_URL = reverse_lazy('account:login')


# Message Tags.
from django.contrib.messages import constants

# NOTE : use them as template tags to keep templates clean and simple.
TAGS = {
    constants.DEBUG: 'alert alert-debug',
    constants.INFO: 'alert alert-info',
    constants.SUCCESS: 'alert alert-success',
    constants.WARNING: 'alert alert-warning',
    constants.ERROR: 'alert alert-danger',
}


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR,'media') 

STATICFILES_DIRS = [os.path.join(BASE_DIR,'static','static_env')]

STATIC_ROOT = os.path.join(BASE_DIR,'static','static_cdn')



# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'


GRAVATAR_PROVIDER_URL = '//www.gravatar.com/avatar'


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOGGING = { 
    'version': 1,
    'disable_existing_loggers': False,
    'filters':{
        'require_debug_false':{
            '()':'django.utils.log.RequireDebugFalse',
        },
    },

    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

