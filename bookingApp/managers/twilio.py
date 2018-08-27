# from django.conf import settings
# from twilio.rest import TwilioRestClient
#
# __author__ = 'eMaM'
#
#
# class TwilioManager():
#     def __init__(self):
#         self.twilio_client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#
#     def create_message(self, body):
#         return self.twilio_client.messages.create(
#             to='+16268645237',
#             from_=settings.FROM,
#             body=body
#         )
