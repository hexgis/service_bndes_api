from .base import *

import io
import environ
import google.auth

from google.cloud import secretmanager

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# False if not in os.environ because of casting above

DEBUG = env('DEBUG')

# Raises Django's ImproperlyConfigured
# exception if SECRET_KEY not in os.environ

SECRET_KEY = os.environ.get('SECRET_KEY')

# START [CloudRun cloud config]
# Attempt to load the Project ID into the environment,
# safely failing on error.
try:
    _, os.environ['GOOGLE_CLOUD_PROJECT'] = google.auth.default()
except google.auth.exceptions.DefaultCredentialsError:
    pass

# Take environment variables from .env file if exists
if os.path.isfile(os.path.join(BASE_DIR, '.env')):
    environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

elif os.environ.get('GOOGLE_CLOUD_PROJECT', None):
    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')
    secrets_name = os.environ.get('SECRETS_NAME')
    secrets_name = \
        f'projects/{project_id}/secrets/{secrets_name}/versions/latest'

    client = secretmanager.SecretManagerServiceClient()
    payload = client.access_secret_version(
        name=secrets_name
    ).payload.data.decode('UTF-8')

    env.read_env(io.StringIO(payload))
else:
    raise Exception(
        'No local .env or GOOGLE_CLOUD_PROJECT detected. No secrets found.'
    )
# END [CloudRun cloud config]


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


# package django-cors-headers configuration
# https://github.com/adamchainz/django-cors-headers

CORS_ALLOW_ALL_ORIGINS = True

# BNDES portal https://developers.bndes.gov.br/
# https://api.bndes.com/api/v2/consultas/

BNDES_URL = os.getenv('BNDES_URL', 'https://api.bndes.com/api/v2/consultas/')

BNDES_URL_VALIDITY = os.getenv('BNDES_URL_VALIDITY', '15')

BNDES_CATEGORY_JSON = json.loads(os.getenv('BNDES_CATEGORY_JSON', '{}'))

BNDES_TOKEN = os.getenv('BNDES_TOKEN', 'secret')

BNDES_ID = os.getenv('BNDES_ID', '')

BNDES_ACCEPTABLE_HTTP_CODES = json.loads(
    os.getenv('BNDES_ACCEPTABLE_HTTP_CODES', '[]'))
