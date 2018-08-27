#!/bin/bash

echo Starting gunicorn
export DJANGO_SETTINGS_MODULE=voyajoy_booking_dj.settings.prod

exec gunicorn voyajoy_booking_dj.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3

#exec python manage.py runserver --settings=voyajoy_booking_dj.settings.prod