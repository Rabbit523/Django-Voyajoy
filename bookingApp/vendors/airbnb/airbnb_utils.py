import json

import requests
from django.conf import settings

__author__ = 'eMaM'


def get_listing_details(listing_id):
    callable_url = settings.AIRBNB_API_URL.format(listing_id)
    try:
        response = requests.get(callable_url, timeout=None)
        return json.loads(response)
    except Exception as e:
        return None
