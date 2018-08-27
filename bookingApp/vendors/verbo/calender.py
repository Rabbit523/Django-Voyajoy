from datetime import datetime, timedelta
import requests
import json

from django.db import transaction

from bookingApp.models import ListingUrlMapping, Listing
from bookingApp.utils import extractNumberFromText

__author__ = 'eMaM'


class VrboCalender():
    def __init__(self, listing_url_mapping):
        self.BASE_URL = 'https://www.vrbo.com/{}'
        self.id = listing_url_mapping.id_vrbo
        self.pattern = r'.*?\[(.*)].*'
        self.listing = listing_url_mapping.listing
        self.HOMEAWAY_LISTING_API='https://dispatch.homeaway.com/bizops/listingSearch/details?systemId={systemId}&propertyId={propertyId}&currency=USD'
        self.VRBO_PRICE_URL ='https://www.vrbo.com/pdp/pricing?listingIds={listingIds}&site=vrbo&arrival={arrival}&departure={departure}&adults={adults}&children={children}&pets=0&isLoggedIn=false&isOnlineBookable=false&acceptsHomeAwayPayments=false&currency=USD&variant=DESKTOP'

    def find_between(self, s, first, last):
        try:
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return ""

    def init_vrbo_http_call(self):
        response = requests.get(self.BASE_URL.format(self.id), timeout=None)
        if response.status_code == 200:
            # if response.status_code == 200 or response.headers.get('HA-urlpath ')=='/'+self.id:
            date_range = self.find_between(response.text, '"dateRange":', ',"maxStayDefault"')
            if date_range:
                date_range = json.loads(str(date_range))
                unit_availability_configuration = self.find_between(response.text, '"unitAvailabilityConfiguration":',
                                                                    '}},"bookability')
                if unit_availability_configuration:
                    unit_availability_configuration = json.loads(str(unit_availability_configuration))
                else:
                    unit_availability_configuration = {}
                return True, self.get_un_available_dates(unit_availability_configuration, date_range)
            return True, list()
        else:
            # mark listing is not available
            listingUrl = ListingUrlMapping.objects.get(id_vrbo=self.id)
            listing = listingUrl.listing
            listing.is_available = False
            listing.save()
            return True, list()

    def get_un_available_dates(self, unit_availability_configuration, date_range):
        if len(unit_availability_configuration) > 0:
            date_format = '%Y-%m-%d'
            availability = unit_availability_configuration['availability']
            # start date
            date_start = date_range['beginDate']
            datetime_start = datetime.strptime(date_start, date_format)
            # end date
            date_end = date_range['endDate']
            datetime_end = datetime.strptime(date_end, date_format)
            check_in_date = datetime_start
            check_out_date = datetime_end

            delta = (check_out_date - check_in_date).days

            availability_calendar = list()

            for x in range(0, delta):
                day = check_in_date + timedelta(days=x)
                if availability[x] == 'N':
                    availability_calendar.append(day.strftime('%d-%m-%y'))
            return availability_calendar
        return []

    @transaction.atomic
    def get_fees(self):
        response = requests.get(self.HOMEAWAY_LISTING_API.format(systemId='vrbo', propertyId=self.id),
                                headers={"Accept-Language": "en-US"}, timeout=None)
        if response.status_code == 200:
            listing = Listing.objects.get(id=self.listing.id)
            listing_data = json.loads(response.text)
            listing_data = listing_data['responseEntity']

            # Get Min stay
            if 'accommodations' in listing_data:
                if 'minStayLow' in listing_data['accommodations']:
                    listing.min_nights = listing_data['accommodations']['minStayLow']
                    listing.save()

                if 'sleeps' in listing_data['accommodations']:
                    listing.max_guests = listing_data['accommodations']['sleeps']
                    listing.save()

            if 'rateDetails' in listing_data:
                if 'rateSections' in listing_data['rateDetails']:
                    for rateSection in listing_data['rateDetails']['rateSections']:
                        # Price
                        if rateSection['title'].lower() == 'My Standard Rate'.lower():
                            if 'rateInfos' in rateSection:
                                for rates in rateSection['rateInfos']:
                                    if rates['title'].lower() == 'Nightly'.lower():
                                        listing.accomodation_fee = float(extractNumberFromText(str(rates['details'])))
                                        listing.save()

                        # Fees
                        if rateSection['title'].lower() == 'fees' :
                            if 'rateInfos' in rateSection:
                                for rates in rateSection['rateInfos']:
                                    if 'details' in rates:
                                        if '%' in rates['details']:
                                            # update listing tax percentage
                                            tax_rate = float(rates['details'].replace('%', ''))
                                            listing.tax_rate_percentage = tax_rate
                                            listing.save()
                                        else:
                                            # delete old data
                                            listing.listing_fees.all().delete()

                                            # calc rate
                                            fees = float(extractNumberFromText(str(rates['details'])))
                                            # insert new data
                                            listing.listing_fees.create(
                                                fees_name=rates['title'],
                                                fees_amount=fees
                                            )



