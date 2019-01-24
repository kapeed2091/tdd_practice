from django.test import TestCase


class TestAddBalance(TestCase):
    customer_id = 'customer1'

    def testcase_add_balance_to_user(self):
        from wallet_v2.models import Account
        Account.create_account(self.customer_id)
        initial_balance = Account.get_balance(self.customer_id)
        Account.add_balance(self.customer_id, 1000)
        balance = Account.get_balance(self.customer_id)
        self.assertEqual(balance - initial_balance, 1000)

    def testcase_add_negative_balance_to_user(self):
        from wallet_v2.models import Account
        Account.create_account(customer_id=self.customer_id)
        with self.assertRaises(Exception):
            Account.add_balance(self.customer_id, -10)

    def testcase_user_has_no_account(self):
        from wallet_v2.models import Account

        with self.assertRaisesMessage(
                Exception, "Customer does not exist"):
            Account.add_balance(self.customer_id, 100)

    def testcase_create_transaction(self):
        from wallet_v2.models import Account, Transaction
        Account.create_account(self.customer_id)

        Account.add_balance(self.customer_id, 1000)
        transactions_count = Transaction.objects.filter(
            account__customer_id=self.customer_id).count()
        self.assertEqual(transactions_count, 1)