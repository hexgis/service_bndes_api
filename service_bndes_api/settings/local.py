from .base import *

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

# debug_toolbar settings

if DEBUG:
    INTERNAL_IPS = ('127.0.0.1',)
    ALLOWED_HOSTS = ['*']

    if os.getenv('ALLOWED_HOSTS'):
        ALLOWED_HOSTS = json.loads(os.environ['ALLOWED_HOSTS'])

    # package django-cors-headers configuration
    # https://github.com/adamchainz/django-cors-headers
    CORS_ALLOW_ALL_ORIGINS = True


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DB_NAME') or 'bndes',
        'USER': os.getenv('DB_USER') or 'bndes',
        'PASSWORD': os.getenv('DB_PASSWORD') or '1234',
        'HOST': os.getenv('DB_HOST') or 'localhost',
        'PORT': os.getenv('DB_PORT') or '5432',
    }
}


# BNDES portal https://developers.bndes.gov.br/
# https://api.bndes.com/api/v2/consultas/

BNDES_URL = os.getenv('BNDES_URL', 'https://api.bndes.com/api/v2/consultas/')

BNDES_URL_VALIDITY = os.getenv('BNDES_URL_VALIDITY', '15')

BNDES_CATEGORY_JSON = json.loads(os.getenv('BNDES_CATEGORY_JSON', '{}'))

BNDES_TOKEN = os.getenv('BNDES_TOKEN', 'secret')

BNDES_ID = os.getenv('BNDES_ID', '')

BNDES_ACCEPTABLE_HTTP_CODES = json.loads(
    os.getenv('BNDES_ACCEPTABLE_HTTP_CODES', '[]'))
