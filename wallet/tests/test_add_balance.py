from django.test import TestCase

from wallet.constants.general import TransactionType


class TestAddBalance(TestCase):
    customer_id = 'customer1'
    account_id = None
    amount_to_add = 10
    transaction_type = TransactionType.CREDIT.value

    def setUp(self):
        from wallet.models import Account
        account_details = Account.create_account(self.customer_id)
        self.account_id = account_details['account_id']

    def testcase_add_balance(self):
        from wallet.models import Account

        prev_balance = Account.get_balance(customer_id=self.customer_id)
        Account.add_balance(self.customer_id, self.amount_to_add)
        balance = Account.get_balance(self.customer_id)

        self.assertEquals(balance, prev_balance+self.amount_to_add)
        self._validate_transaction_db_state()

    def testcase_add_negative_balance(self):
        from wallet.models import Account
        with self.assertRaises(Exception):
            Account.add_balance(self.customer_id, -10)

    def testcase_add_float_balance(self):
        from wallet.models import Account
        with self.assertRaises(Exception):
            Account.add_balance(self.customer_id, float(10.5))

    def _validate_transaction_db_state(self):
        from wallet.models import Transaction
        transactions = \
            Transaction.objects.filter(account__customer_id=self.customer_id)

        transaction = transactions[0]

        self.assertEquals(transaction.account.customer_id, self.customer_id)
        self.assertEquals(transaction.amount, self.amount_to_add)
        self.assertEquals(transaction.transaction_type, self.transaction_type)
