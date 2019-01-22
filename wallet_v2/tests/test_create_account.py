from django.test import TestCase


class TestCreateAccount(TestCase):

    def testcase_create_account(self):
        customer_id = 'customer1'

        account_details = Account.create_account(customer_id)
        self.assertEqual(account_details['customer_id'], customer_id)
