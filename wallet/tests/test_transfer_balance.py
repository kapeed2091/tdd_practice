from django.test import TestCase
from wallet.models import Account


class TestTransferBalance(TestCase):
    sender_customer_id = 'sender'
    receiver_customer_id = 'receiver'

    def setUp(self):
        sender_account_details = Account.create_account(self.sender_customer_id)
        receiver_account_details = Account.create_account(
            self.receiver_customer_id)

        Account.add_balance(self.sender_customer_id, 50)
        Account.add_balance(self.receiver_customer_id, 30)

    def testcase_transfer_balance(self):
        sender_old_balance = Account.get_balance(self.sender_customer_id)
        receiver_old_balance = Account.get_balance(self.receiver_customer_id)

        Account.transfer_balance(
            self.sender_customer_id, self.receiver_customer_id, 10)

        sender_new_balance = Account.get_balance(self.sender_customer_id)
        receiver_new_balance = Account.get_balance(self.receiver_customer_id)

        self.assertEquals(sender_old_balance, sender_new_balance+10)
        self.assertEquals(receiver_old_balance, receiver_new_balance-10)

    def testcase_transfer_more_than_sender_balance(self):
        sender_old_balance = Account.get_balance(self.sender_customer_id)
        receiver_old_balance = Account.get_balance(self.receiver_customer_id)

        with self.assertRaises(Exception):
            Account.transfer_balance(
                self.sender_customer_id, self.receiver_customer_id, 60)

