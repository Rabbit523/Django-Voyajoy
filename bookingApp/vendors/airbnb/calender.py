import json
from datetime import timedelta, datetime

import requests
from django.db import transaction

from bookingApp.models import Listing

__author__ = 'eMaM'


class AirbnbCalender():
    def __init__(self, listing_id,listing_mapping_url, arrival_date=None, depature_date=None):
        self.listing_id = listing_id
        self.listing_mapping_url = listing_mapping_url
        self.CALENDER_URL = 'https://www.airbnb.com/api/v2/calendar_months?_format=with_conditions&listing_id={listing_id}&month={month}&year={year}&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=USD&locale=en'
        self.PRICE_QUOTS = 'https://api.airbnb.com/v2/pricing_quotes?client_id=3092nxybyb0otqw18e8nh5nty&listing_id={listing_id}'
        self.LISTING = 'https://api.airbnb.com/v2/listings/{listing_id}?client_id=3092nxybyb0otqw18e8nh5nty&locale=en-US&currency=USD&_format=v1_legacy_for_p3&_source=mobile_p3'

    def get_un_available_dates(self):
        formatted_date = datetime.today()
        response = requests.get(
            self.CALENDER_URL.format(listing_id=self.listing_mapping_url, month=formatted_date.month, year=formatted_date.year),
            timeout=None)
        unavailable_dates = []
        if response.status_code == 200:
            calender_date = json.loads(response.text)
            if 'calendar_months' in calender_date:
                if 'days' in calender_date['calendar_months']:
                    for available_date in calender_date['calendar_months']['days']:
                        if not available_date['available']:
                            unavailable_dates.append(available_date['date'].strftime('%d-%m-%y'))
        return unavailable_dates

    def get_price(self):
        response = requests.get(self.PRICE_QUOTS.format(listing_id=self.listing_mapping_url), timeout=None)
        if response.status_code == 200:
            data = json.loads(response.text)
        pass

    @transaction.atomic
    def get_listing_fees(self):
        response = requests.get(self.LISTING.format(listing_id=self.listing_mapping_url), timeout=None)
        if response.status_code == 200:
            data = json.loads(response.text)
            price = None
            if 'price' in data['listing']:
                price = data['listing']['price']

            cleaning_fee = None
            if 'listing_cleaning_fee_native' in data['listing']:
                cleaning_fee = data['listing']['listing_cleaning_fee_native']

            security_deposit = None
            if 'listing_security_deposit_native' in data['listing']:
                security_deposit = data['listing']['listing_security_deposit_native']

            listing_obj = Listing.objects.get(id=self.listing_id)
            if price:
                listing_obj.accomodation_fee = price

            min_nights = 0
            if 'min_nights'  in data['listing']:
                min_nights = data['listing']['min_nights']

            max_adults = 0
            if 'person_capacity' in data['listing']:
                max_adults = data['listing']['person_capacity']

            listing_obj.min_nights = min_nights
            listing_obj.max_guests = max_adults
            listing_obj.save()

            listing_obj.listing_fees.all().delete()

            if cleaning_fee:
                listing_obj.listing_fees.create(
                    fees_name='Cleaning Fees',
                    fees_amount=cleaning_fee,
                )

            if security_deposit:
                listing_obj.listing_fees.create(
                    fees_name='Security Deposit',
                    fees_amount=security_deposit,
                )
