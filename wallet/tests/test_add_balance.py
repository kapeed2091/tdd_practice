from django.test import TestCase


class TestAddBalance(TestCase):
    customer_id = 'customer1'

    def testcase_add_balance(self):
        from wallet.models import Account

        Account.create_account(self.customer_id)
        initial_balance = Account.get_balance(self.customer_id)
        Account.add_balance(self.customer_id, 1000)
        balance = Account.get_balance(self.customer_id)

        self.assertEqual(balance - initial_balance, 1000, "Incorrect balance")
