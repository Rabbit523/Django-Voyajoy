from bookingApp.models import Billing

__author__ = 'eMaM'

class VoyajoyPayment():


    def create_billing(self, reservation, braintree_transaction,user):
        try:
            r = Billing(
                customer_id = str(braintree_transaction.customer['id']),
                auth_user = user,
                reservation = reservation,
                status = True,
                desc = braintree_transaction.status ,
                payment_ref = braintree_transaction.id
            )

            r.save()
            return True,r
        except Exception as e:
            print 'Error during create voyajoy payment for Braintree transaction id {} cause {}'.format(braintree_transaction.id, str(e))
            return False, str(e)