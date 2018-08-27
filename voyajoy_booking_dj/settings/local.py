__author__ = 'eMaM'
from base import *
from base import _required_env


DEBUG= False
ALLOWED_HOSTS = ['127.0.0.1','localhost']

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': _required_env('PG_DB'),
#         'USER': _required_env('PG_USER'),
#         'PASSWORD': _required_env('PG_PASS'),
#         'HOST': _required_env('PG_HOST'),  # '127.0.0.1'
#         'PORT': _required_env('PG_PORT'),  # '5556'
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'aaa',
        'USER': 'postgres',
        'PASSWORD': 'whrnrxhddlf',
        'HOST': '127.0.0.1',  # '127.0.0.1'
        'PORT': '5432',  # '5556'
    }


}


# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, "static"),
# )

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
