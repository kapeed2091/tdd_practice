from django.test import TestCase


class TestGetBalance(TestCase):
    customer_id = 'customer1'

    def testcase_get_balance(self):
        from wallet_v2.models import Account
        Account.create_account(self.customer_id)
        balance = Account.get_balance(self.customer_id)
        self.assertEqual(balance, 0)
        Account.add_balance(self.customer_id, 100)
        balance = Account.get_balance(self.customer_id)
        self.assertEqual(balance, 100)

    def testcase_get_balance_without_account(self):
        from wallet_v2.models import Account
        with self.assertRaisesMessage(
                Exception, "Customer does not exist"):
            Account.get_balance(self.customer_id)
