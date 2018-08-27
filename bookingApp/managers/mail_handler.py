from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import  send_mail
from django.template.loader import render_to_string

__author__ = 'eMaM'


def __send_email_(subject, body, to_emails, bcc_email):
    # msg = EmailMessage(
    #     subject=subject,
    #     from_email=settings.SENDER,
    #     body=body,
    #     bcc=bcc_email,
    #     to=to_emails
    # )
    # msg.content_subtype = "html"
    # msg.send()
    send_mail(subject=subject,message=body,from_email=settings.DEFAULT_FROM_EMAIL,recipient_list=to_emails,html_message=body)


def send_reservation_requrest_to_owner(reservation,request):
    subject = '%s wants to rent from %s through %s' % (
        reservation.renter.get_full_name(),
        reservation.arrival_date.strftime("%m/%d/%Y"),
        reservation.departure_date.strftime("%m/%d/%Y")
    )

    body = render_to_string('mailer/owner_reservation_request.html', context={'reservation': reservation},request=request)
    # to = [reservation.listing.owner_email]
    to = ['inquiries@voyajoy.com']
    # bcc = ['inquiries@voyajoy.com','eng.ahmed_2222@hotmail.com']
    __send_email_(subject=subject, body=body, to_emails=to, bcc_email=None)


def send_renter_request_notification(reservation,request):
    subject = 'Your Voyajoy Booking Request from %s through %s ' % (

        reservation.arrival_date.strftime("%m/%d/%Y"),
        reservation.departure_date.strftime("%m/%d/%Y"),
        # reservation.listing.auth_user.get_full_name(),
    )

    body = render_to_string('mailer/reservation_request_confirmation.html', context={'reservation': reservation},request=request)
    to = [reservation.renter.email]
    # bcc = ['inquiries@voyajoy.com']
    # to = ['emam151987@gmail.com']
    __send_email_(subject=subject, body=body, to_emails=to, bcc_email=None)


def send_reservation_approved_confirmation(reservation,request):
    subject = 'Your Voyajoy Booking Request was approved for %s through %s' % (
        reservation.arrival_date.strftime("%m/%d/%Y"),
        reservation.departure_date.strftime("%m/%d/%Y"),
    )

    body = render_to_string('mailer/reservation_approved_confirmation.html', context={'reservation': reservation},request=request)
    to = [reservation.renter.email]
    # bcc = ['inquiries@voyajoy.com']
    __send_email_(subject=subject, body=body, to_emails=to, bcc_email=None)


def send_reservation_denied_confirmation(reservation,request):
    subject = 'Your Voyajoy Booking Request for %s through %s' % (
        reservation.arrival_date.strftime("%m/%d/%Y"),
        reservation.departure_date.strftime("%m/%d/%Y"),
    )
    body = render_to_string('mailer/reservation_denied_confirmation.html', context={'reservation': reservation},request=request)
    to = [reservation.renter.email]
    # bcc = ['inquiries@voyajoy.com']
    __send_email_(subject=subject, body=body, to_emails=to, bcc_email=None)



