from django.test import TestCase


class TestCreateAccount(TestCase):

    def testcase_create_account(self):
        customer_id = 'customer1'
        from wallet_v2.models import Account
        account_details = Account.create_account(customer_id)
        self.assertEqual(account_details['customer_id'], customer_id)

    def testcase_different_account_for_different_users(self):
        customer_id_1 = 'customer1'
        customer_id_2 = 'customer2'
        from wallet_v2.models import Account
        account_id_1 = Account.create_account(customer_id_1)['account_id']
        account_id_2 = Account.create_account(customer_id_2)['account_id']

        self.assertNotEqual(account_id_1, account_id_2, 'AccountIds Matched.!')
