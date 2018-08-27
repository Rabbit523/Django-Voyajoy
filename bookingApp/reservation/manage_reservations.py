import datetime

# from bookingApp.managers.twilio import TwilioManager
import decimal

from bookingApp.managers.mail_handler import send_reservation_approved_confirmation, \
    send_reservation_denied_confirmation
from bookingApp.models import ReservationSmsCounter, Reservation

__author__ = 'eMaM'


class ReservationManagement():
    def __init__(self, renter=None, listing=None, arrival_date=None, departure_date=None, no_of_adults=None,
                 no_of_childs=None, total=None):
        self.listing = listing
        self.arrival_date = arrival_date
        self.departure_date = departure_date
        self.no_of_adults = no_of_adults
        self.no_of_childs = no_of_childs
        self.renter = renter
        self.renter_fees = total
        self.no_of_night = self.__get_no_of_nights()

    def is_valid_booking_request(self):
        if self.listing.min_nights > self.no_of_night:
            return False, 'Minimum nighties are {}'.format(self.listing.min_nights)

        if self.no_of_adults < self.listing.max_guests:
            return False, 'Maximum Guests are {}'.format(self.listing.max_guests)

        return True, 'Valid'

    def __get_no_of_nights(self):
        if self.arrival_date and self.departure_date:
            self.arrival_date = self.__get_datetime(self.arrival_date)
            self.departure_date = self.__get_datetime(self.departure_date)
            days_diff = self.__get_date_delta_days(self.arrival_date, self.departure_date)
            if days_diff == 0:
                days_diff = 1
            return days_diff
        return 0

    def update_reservation_status(self, id, request, is_accepted=False):
        if is_accepted:
            return self.__accept_reservation(id=id, request=request)
        return self.__reject_reservation(id=id, request=request)

    def create_booking_request(self):
        try:
            reservation_counter = ReservationSmsCounter.objects.get(auth_user=self.listing.auth_user)
            counter = reservation_counter.counter
            counter += 1
            reservation_counter.counter = counter
            reservation_counter.save()
        except Exception as e:
            print 'error:', str(e), type(e)
            reservation_counter = ReservationSmsCounter(auth_user=self.listing.auth_user, counter=1)
            reservation_counter.save()
            counter = 1

        booking_prices_details = self.__calculate_price(self.no_of_night)
        try:
            r = Reservation(
                listing=self.listing,
                renter=self.renter,
                arrival_date=self.arrival_date,
                departure_date=self.departure_date,
                no_of_adults=self.no_of_adults,
                no_of_childs=self.no_of_childs,
                num_nights=self.no_of_night,
                cleaning_fee=0,
                discounted_rate=booking_prices_details['discount_rate'],
                security_deposit=0,
                taxes=booking_prices_details['taxes'],
                tax_rate=booking_prices_details['tax_rate'],
                total=booking_prices_details['total'],
                total_discount=booking_prices_details['total_discount'],
                rental_fee_total_with_discount=booking_prices_details['rental_fee_total_with_discount'],
                rental_fee_total_without_discount=booking_prices_details['rental_fee_total_without_discount'],
                reservation_reply_id=counter,
                owner_fees=self.renter_fees

            )
            r.save()

            for fees in self.listing.listing_fees.all():
                r.reservation_fees.create(
                    fees_name=fees.fees_name,
                    fees_amount=fees.fees_amount
                )

            return True, r
        except Exception as e:
            print str(e)
            return False, str(e)

    def __calculate_price(self, no_of_nights):
        booking_prices_details = {}
        total = float(0)
        discount_rate = float('{0:.2f}'.format(self.listing.discount_rate))
        booking_prices_details['discount_rate'] = float('{0:.2f}'.format(discount_rate))

        tax_rate_percentage = self.listing.tax_rate_percentage
        booking_prices_details['tax_rate'] = float('{0:.2f}'.format(tax_rate_percentage))

        accomodation_fee = self.listing.accomodation_fee
        booking_prices_details['accomodation_fee'] = float('{0:.2f}'.format(accomodation_fee))

        discount_per_night = discount_rate / 100 * accomodation_fee
        total_discount = discount_per_night * no_of_nights
        booking_prices_details['total_discount'] = float('{0:.2f}'.format(total_discount))

        rental_fee_total_without_discount = accomodation_fee * no_of_nights
        booking_prices_details['rental_fee_total_without_discount'] = float(
            '{0:.2f}'.format(rental_fee_total_without_discount))

        rental_fee_total_with_discount = rental_fee_total_without_discount - total_discount
        booking_prices_details['rental_fee_total_with_discount'] = float(
            '{0:.2f}'.format(rental_fee_total_with_discount))

        if rental_fee_total_with_discount < rental_fee_total_without_discount:
            total = rental_fee_total_with_discount
        else:
            total = rental_fee_total_without_discount

        fees = float(0)
        for listing_fees in self.listing.listing_fees.all():
            fees += float('{0:.2f}'.format(listing_fees.fees_amount))

        total = float('{0:.2f}'.format(total))
        total += fees

        tax_rate_percentage = float('{0:.2f}'.format(tax_rate_percentage))
        tax = (total * tax_rate_percentage) / 100
        booking_prices_details['taxes'] = float('{0:.2f}'.format(tax))

        total += (total * tax_rate_percentage) / 100
        booking_prices_details['total'] = float('{0:.2f}'.format(total))

        # booking_prices_details['total'] = 0.07

        return booking_prices_details

    def __get_datetime(self, date_string):
        date_format = '%m/%d/%Y'
        date = datetime.datetime.strptime(date_string, date_format)
        return date;

    def __get_date_delta_days(self, start, end):
        delta = (end - start).days
        return delta

    def __send_inquiry_text(self, reservation):
        user = reservation.listing.owner
        renter = reservation.renter.get_full_name()
        counter = reservation.reservation_reply_id
        reply_id = counter
        template = 'Hi {owner}, {renter} wants to stay at your home on {arrival} until {departure} ({days}) for ${price}. Reply with {reply_id} to accept {renter}\'s request'
        message = template.format(
            owner=user.firstName,
            renter=renter,
            days='%s night' % reservation.numNights if reservation.numNights == 1 else '%s nights' % reservation.numNights,
            arrival=self.arrival_date,
            departure=self.departure_date,
            price=reservation.total,
            reply_id=reply_id
        )

        # Send SMS
        # TwilioManager().create_message(body=message)

    def __accept_reservation(self, id, request):
        try:
            reservation = Reservation.objects.get(id=id)

            if reservation.approved:
                return False, 'Reservation Accepted before. Thanks!', reservation

            if reservation.rejected:
                return False, 'Reservation Rejected before. Thanks!', reservation

            reservation.approved = True
            reservation.save()
            # send Approved email
            send_reservation_approved_confirmation(reservation=reservation, request=request)
            return True, 'Reservation Accepted. Thanks!', reservation
        except Exception as e:
            return False, 'Error during accept reservation with ID {} , cause : {}'.format(id, str(e))

    def __reject_reservation(self, id, request):
        try:
            reservation = Reservation.objects.get(id=id)
            if reservation.approved:
                return False, 'Reservation Accepted before. Thanks!', reservation

            if reservation.rejected:
                return False, 'Reservation Rejected before. Thanks!', reservation
            reservation.rejected = True

            reservation.save()
            # send Reject email
            send_reservation_denied_confirmation(reservation=reservation, request=request)
            return True, 'Reservation Rejected .Thanks!', reservation
        except Exception as e:
            return False, 'Error during reject reservation with ID {} , cause : {}'.format(id, str(e))

    def getReservation(self, id):
        return Reservation.objects.get(id=id)
