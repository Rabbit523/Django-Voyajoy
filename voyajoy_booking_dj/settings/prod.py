__author__ = 'eMaM'
from base import *

import braintree

DEBUG = False
ALLOWED_HOSTS = ['stays.voyajoy.com']

BRAINTREE_GATEWAY = dict(
    environment=braintree.Environment.Production,
    merchant_id='yqhsqsm8h9qjrq23',
    public_key='vt4qs2nmkjk82xfy',
    private_key='cd5d9ef292100567e8c9d0e032d45876'
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'voyajoy_booking',
        'USER': 'voyajoy@voyajoybookingpsqlprod',
        'PASSWORD': 'Rb9FCvzPKD6eauXY',
        'HOST': 'voyajoybookingpsqlprod.postgres.database.azure.com',  # '127.0.0.1'
        'PORT': '5432',  # '5556'
    }


}


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')