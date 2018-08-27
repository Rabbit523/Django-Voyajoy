"""
WSGI config for voyajoy_booking_dj project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.core.exceptions import ImproperlyConfigured

def _required_env(name):
    try:
        value = os.environ[name]
        if not value:
            raise KeyError
        return value
    except KeyError:
        raise ImproperlyConfigured('Missing env variable: "{}"'.format(name))

# ENV = _required_env('ENV')
# print "voyajoy_booking_dj.settings.{}".format(ENV)

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "voyajoy_booking_dj.settings.{}".format(ENV))
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "voyajoy_booking_dj.settings.staging")

application = get_wsgi_application()
