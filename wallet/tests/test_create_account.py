from django.test import TestCase


class TestCreateAccount(TestCase):

    def test_create_account(self):
        from wallet.models import Account
        customer_id = 'customer1'
        account_details = Account.create_account(customer_id)

        self.assertEqual(account_details['customer_id'], customer_id,
                         "customer_id mismatch")
