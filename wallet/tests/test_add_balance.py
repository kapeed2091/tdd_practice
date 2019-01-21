from django.test import TestCase


class TestAddBalance(TestCase):
    customer_id = 'customer1'
    account_id = None

    def setUp(self):
        from wallet.models import Account
        account_details = Account.create_account(self.customer_id)
        self.account_id = account_details['account_id']

    def testcase_add_balance(self):
        from wallet.models import Account

        prev_balance = Account.get_balance(customer_id=self.customer_id)
        Account.add_balance(self.customer_id, 10)
        balance = Account.get_balance(self.customer_id)

        self.assertEquals(balance, prev_balance+10)

    def testcase_add_negative_balance(self):
        from wallet.models import Account
        with self.assertRaises(Exception):
            Account.add_balance(self.customer_id, -10)

    def testcase_add_float_balance(self):
        from wallet.models import Account
        with self.assertRaises(Exception):
            Account.add_balance(self.customer_id, 10.5)
