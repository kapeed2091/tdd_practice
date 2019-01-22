from django.test import TestCase


class TestCreateAccount(TestCase):

    def testcase_create_account(self):
        from wallet.models import Account
        customer_id = 'customer1'
        account_details = Account.create_account(customer_id)

        self.assertEqual(account_details['customer_id'], customer_id,
                         "customer_id mismatch")

    def testcase_different_accounts_for_different_users(self):
        from wallet.models import Account
        customer_1_id = 'customer1'
        customer_2_id = 'customer2'

        customer_1_details = Account.create_account(customer_1_id)
        customer_2_details = Account.create_account(customer_2_id)

        self.assertNotEqual(
            customer_1_details['account_id'], customer_2_details['account_id'],
            "same account numbers for different accounts")
