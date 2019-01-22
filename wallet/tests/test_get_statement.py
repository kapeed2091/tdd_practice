from django.test import TestCase
from wallet.models import Account


class TestGetStatement(TestCase):
    sender_customer_id = 'sender'
    receiver_customer_id = 'receiver'

    def setUp(self):
        Account.create_account(self.sender_customer_id)
        Account.create_account(self.receiver_customer_id)

    def testcase_get_statement(self):
        from wallet.models import Transaction
        transactions_list = Transaction.get_statement(self.sender_customer_id)

        self.assertEquals(transactions_list, [])