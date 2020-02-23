from .local import *

DEBUG = True

ALLOWED_HOSTS = config('ALLOWED_HOSTS',
						cast=lambda x:[s.strip() for s in x.split(',')],
						default='127.0.0.1,localhost')

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Email Config.
EMAIL_HOST = '' # Eg. smtp.gmail.com
EMAIL_HOST_USER = '' # Eg. kraft.developer@gmail.com
EMAIL_HOST_PASSWORD = '' # password for kraft.developer@gmail.com
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'test@test.com' # Eg. kraft.developer@gmail.com (ie.email from.)

ACCOUNT_EMAIL_SUBJECT_PREFIX = 'Test Subject'


EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'emails')

ENABLE_SSL = False