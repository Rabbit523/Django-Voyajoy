from base import *
__author__ = 'eMaM'

import braintree

ALLOWED_HOSTS = ['stays-staging.voyajoy.com','127.0.0.1']

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'stag_booking',
        'USER': 'voyajoy@voyajoy-booking-staging-pg',
        'PASSWORD': 'oIbkdPGJrXyo3oIM',
        'HOST': 'voyajoy-booking-staging-pg.postgres.database.azure.com',  # '127.0.0.1'
        'PORT': '5432',  # '5556'
    }
}

#
BRAINTREE_GATEWAY = dict(
    environment=braintree.Environment.Sandbox,
    merchant_id='njpzm7qspw6tks2z',
    public_key='9vmt4kct7ty5s92n',
    private_key='60e0214f6426274ac076f2838ba3676b'
)




STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')



