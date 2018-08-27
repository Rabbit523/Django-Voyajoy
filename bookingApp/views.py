# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import sys
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.response import HttpResponse, Http404
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import render_to_string
from django.urls.base import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from bookingApp.forms import ReservationForm
from bookingApp.managers.mail_handler import send_reservation_requrest_to_owner, send_renter_request_notification
from bookingApp.models import Region, Review, Listing, Reservation
from bookingApp.payment.braintree_manager import BraintreeManager
from bookingApp.payment.voyjoy_payment import VoyajoyPayment
from bookingApp.reservation.manage_reservations import ReservationManagement
from bookingApp.vendors.airbnb.calender import AirbnbCalender
from bookingApp.vendors.verbo.calender import VrboCalender


def index(request):
    template = 'index.html'
    context = {'random_listing': Listing.objects.all().order_by('?')[:8],
               'region_query_set': Region.objects.filter(is_active=True).order_by("name").order_by("-weight")}
    return render(request=request, template_name=template, context=context)


def careers(request):
    template = 'careers.html'
    context = {
        'region_query_set': Region.objects.filter(is_active=True).order_by("name").order_by("-weight")
    }
    return render(request=request, template_name=template, context=context)


def tos(request):
    template = 'tos.html'
    context = {
        'region_query_set': Region.objects.filter(is_active=True).order_by("name").order_by("-weight")
    }
    return render(request=request, template_name=template, context=context)


def policy(request):
    template = 'policy.html'
    context = {
        'region_query_set': Region.objects.filter(is_active=True).order_by("name").order_by("-weight")
    }
    return render(request=request, template_name=template, context=context)


def about(request):
    template = 'about.html'
    context = {
        'region_query_set': Region.objects.filter(is_active=True).order_by("name").order_by("-weight")
    }
    return render(request=request, template_name=template, context=context)


def browse_region(request, slug):
    template = 'region.html'
    listing_list = Listing.objects.filter(region__slug=slug)
    paginator = Paginator(listing_list, 8)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:

        listings = paginator.page(page)

    except PageNotAnInteger:

        # If page is not an integer, deliver first page.

        listings = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        listings = paginator.page(paginator.num_pages)

    context = {
        'region_listings': listings,
        'region': Region.objects.get(slug=slug),
        'region_query_set': Region.objects.filter(is_active=True).order_by("name").order_by("-weight")
    }
    return render(request=request, template_name=template, context=context)


def room_detail(request, slug):
    template = 'room_details.html'
    listing = Listing.objects.prefetch_related().get(slug=slug)
    listing_mapping = listing.map_list.get()
    unavailable_dates = []
    if listing_mapping.is_airbnb:
        airbnb_calender = AirbnbCalender(listing_mapping_url=listing_mapping.is_airbnb, listing_id=listing.id)
        unavailable_dates = airbnb_calender.get_un_available_dates()
        # Do Fees and price update
        airbnb_calender.get_listing_fees()

    elif listing_mapping.is_vrbo:
        vrbo_client = VrboCalender(listing_mapping)
        vrboCalenderStatus = vrbo_client.init_vrbo_http_call()
        if vrboCalenderStatus[0]:
            unavailable_dates = vrboCalenderStatus[1]
            # do fees
            vrbo_client.get_fees()
        else:
            raise Http404

    reservation_form = ReservationForm(no_of_agent=listing.max_guests)

    context = {
        'listing': listing,
        'unavailable_dates': unavailable_dates,
        'form': reservation_form,
        'region_query_set': Region.objects.filter(is_active=True).order_by("name").order_by("-weight")
    }

    return render(request=request, template_name=template, context=context)


@require_http_methods('GET')
@login_required
def booking_request(request):
    # valid = False
    # msg = 'Error : {}'
    #
    error = False

    error_msg = request.session.get('error_msg', None)
    if error_msg:
        error = True

    listing_id = request.GET.get('listing_id', None)
    arrival_date = request.GET.get('arrival_date', None)
    departure_date = request.GET.get('departure_date', None)
    no_of_adult = request.GET.get('no_of_guest', None)
    no_of_child = request.GET.get('no_of_guest_child', 0)
    total = request.GET.get('total', 0)
    # Retrieve listing info
    listing = Listing.objects.get(id=listing_id)

    context = {
        'listing': listing,
        'arrival_date': arrival_date,
        'departure_date': departure_date,
        'no_of_adult': no_of_adult,
        'no_of_child': no_of_child,
        'total': total,
        'region_query_set': Region.objects.filter(is_active=True).order_by("name").order_by("-weight"),
        'msg': error_msg,
        'error': error
    }

    template = 'cart/booking_requests.html'
    return render(request, template_name=template, context=context)


def booking_review(request):
    pass


@login_required
@require_http_methods('GET')
def booking_list(request):
    template = 'cart/reservation_history.html'
    reservation_list = Reservation.objects.filter(renter=request.user).order_by('-created_at')
    return render(request=request, template_name=template, context={'reservation_list': reservation_list,
                                                                    'region_query_set': Region.objects.filter(
                                                                        is_active=True).order_by(
                                                                        "name").order_by("-weight")})


@login_required
@require_http_methods(['POST', 'GET'])
def checkout(request):
    template = 'cart/cart.html'

    listing_id = request.GET.get('listing_id', None)
    arrival_date = request.GET.get('arrival_date', None)
    departure_date = request.GET.get('departure_date', None)
    no_of_adult = request.GET.get('no_of_guest', None)
    no_of_child = request.GET.get('no_of_guest_child', 0)
    total = request.GET.get('total', 0)
    # Retrieve listing info
    listing = Listing.objects.get(id=listing_id)

    # Manage Reservation
    reservation_manager = ReservationManagement(renter=request.user, listing=listing, arrival_date=str(arrival_date),
                                                departure_date=str(departure_date), no_of_adults=no_of_adult,
                                                no_of_childs=no_of_child, total=total)

    # Process on booking
    reservation = reservation_manager.create_booking_request()
    if reservation[0]:
        request.session['braintree_client_token'] = BraintreeManager().get_client_token(auth_user=request.user)
    else:

        msg_err = reservation[1]
        request.session['error_msg'] = msg_err
        return redirect(reverse('booking_request'))
    return render(request=request, template_name=template, context={'reservation': reservation[1],
                                                                    'region_query_set': Region.objects.filter(
                                                                        is_active=True).order_by(
                                                                        "name").order_by("-weight")})


@login_required
@require_http_methods('POST')
def complete_checkout(request):
    reservation = Reservation.objects.get(pk=request.POST.get('reservation_id', None))
    if not reservation:
        return HttpResponse(
            json.dumps({'is_valid': False, 'msg': 'Unable to retrieve reservation'}, ensure_ascii=False))

    if reservation.renter != request.user:
        return HttpResponse(json.dumps({'is_valid': False, 'msg': 'Invalid Authorization '}, ensure_ascii=False))

    payment_status = BraintreeManager().create_payment(auth_user=request.user, amount=reservation.total,
                                                       payment_nonce=request.POST.get('payment_method_nonce', None))

    if payment_status[0]:
        msg = 'Payment successfully done'
        # create Billing
        bill_obj = VoyajoyPayment().create_billing(reservation=reservation, braintree_transaction=payment_status[1],
                                                   user=request.user)

        print '------------ voyajoy payment'

        print bill_obj

        print '------------end voyajoypayment=========='

        if bill_obj[0]:
            # send email notification to owner
            send_reservation_requrest_to_owner(reservation=reservation, request=request)

            # send payment notification to renter
            send_renter_request_notification(reservation=reservation, request=request)

            return HttpResponse(json.dumps({'is_valid': True, 'msg': msg}, ensure_ascii=False))

        else:
            msg += '[Warning]' + bill_obj[1]
            return HttpResponse(json.dumps({'is_valid': True, 'msg': msg}, ensure_ascii=False))

    return HttpResponse(json.dumps({'is_valid': False, 'msg': payment_status[1]}, ensure_ascii=False))


@csrf_exempt
def viewBooking(request, reservation_id):
    template = 'cart/reservation_confirmation.html'
    reservation = ReservationManagement().getReservation(id=reservation_id)
    context = {
        'region_query_set': Region.objects.filter(is_active=True).order_by(
            "name").order_by("-weight"),
        "reservation": reservation
    }
    return render(request=request, template_name=template, context=context)


@require_http_methods('POST')
def AcceptBooking(request, reservation_id):
    reservation_status = ReservationManagement().update_reservation_status(id=reservation_id, request=request,
                                                                           is_accepted=True)
    context = {
        "valid": reservation_status[0],
        "msg": reservation_status[1],
    }
    html = render_to_string('base/notifications.html', context=context)
    context['html'] = html
    return HttpResponse(json.dumps(context, ensure_ascii=False))


@require_http_methods('POST')
def RejectBooking(request, reservation_id):
    reservation_status = ReservationManagement().update_reservation_status(id=reservation_id, request=request,
                                                                           is_accepted=False)

    context = {
        "valid": reservation_status[0],
        "msg": reservation_status[1],
    }
    html = render_to_string('base/notifications.html', context=context)
    context['html'] = html
    return HttpResponse(json.dumps(context, ensure_ascii=False))


def handler404(request):
    return render(request, '500.html', status=404)


def handler500(request):
    if request.is_ajax():
        data = {
            'type':sys.exc_info()
        }
        return HttpResponse(json.dumps(data),status=500)
    return render(request, '500.html', status=500)
