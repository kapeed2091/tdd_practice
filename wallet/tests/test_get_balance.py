from django.test import TestCase


class TestGetBalance(TestCase):
    customer_id = 'customer1'

    def testcase_get_new_user_account_balance(self):
        from wallet.models import Account
        Account.create_and_return_account(self.customer_id)
        balance = Account.get_account_balance(self.customer_id)
        self.assertEquals(balance, 0,
                          'Incorrect balance for new account')

    def testcase_get_balance_without_customer_account(self):
        from wallet.models import Account
        self.assertRaises(Account.DoesNotExist,
                          lambda : Account.get_account_balance(
                              self.customer_id))
