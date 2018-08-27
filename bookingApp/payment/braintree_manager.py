import braintree
import decimal
from django.conf import settings

from bookingApp.models import Billing

__author__ = 'eMaM'


class BraintreeManager():
    def __init__(self):
        braintree.Configuration.configure(settings.BRAINTREE_GATEWAY['environment'],
                                          merchant_id=settings.BRAINTREE_GATEWAY['merchant_id'],
                                          public_key=settings.BRAINTREE_GATEWAY['public_key'],
                                          private_key=settings.BRAINTREE_GATEWAY['private_key'])

    def get_client_token(self, auth_user):
        # billing_query_set = Billing.objects.filter(auth_user=auth_user)
        # if billing_query_set:
        #     return self.__generate_client_token(billing_query_set[0].customer_id)
        return self.__generate_client_token()

    def __generate_client_token(self, braintree_customer_id=None):
        if braintree_customer_id:
            return braintree.ClientToken.generate({
                "customer_id": braintree_customer_id
            })
        else:
            return braintree.ClientToken.generate()

    def create_payment(self, auth_user, amount, payment_nonce):
        # billing_query_set = Billing.objects.filter(auth_user=auth_user)
        # if billing_query_set:
        #     return self.__create_payment_transaction(customer_id=billing_query_set[0].customer_id, amount=amount)
        # else:
        result = self.__creat_braintree_customer(auth_user=auth_user, payment_nonce=payment_nonce)

        print '--------- create customer ------------'
        print result
        print '---------end create customer ---------'
        if result[0]:
            customer_id = result[1]
            return self.__create_payment_transaction(customer_id=customer_id, amount=amount)
        else:
            return False, result[1]

    def __create_payment_transaction(self, customer_id, amount):
        result = braintree.Transaction.sale({
            'customer_id': customer_id,
            'amount': str(amount),
            'options': {
                "submit_for_settlement": True
            },
        })

        print '--------------- create payment ----------------'
        print result
        print '--------------end create payment --------------'

        if result.is_success:
            return True, result.transaction
        elif result.errors.deep_errors:
            return result.is_success, result.errors.deep_errors
        else:
            return False, result.transaction.processor_response_code + ' ' + result.transaction.processor_response_text

    def __creat_braintree_customer(self, auth_user, payment_nonce):
        result = braintree.Customer.create({
            'first_name': auth_user.first_name,
            'last_name': auth_user.last_name,
            'email': auth_user.email,
            'phone': auth_user.phone if hasattr(auth_user, 'phone') else '',
            "credit_card": {
                "payment_method_nonce": payment_nonce,
                "options": {
                    "verify_card": True,
                }
            }
        })

        if result.is_success:
            return True, result.customer.id
        return False, result.message
