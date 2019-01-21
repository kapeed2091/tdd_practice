from django.test import TestCase
from wallet.models import Account


class TestTransferBalance(TestCase):
    sender_customer_id = 'sender'
    receiver_customer_id = 'receiver'

    def setUp(self):
        Account.create_account(self.sender_customer_id)
        Account.create_account(self.receiver_customer_id)

        Account.add_balance(self.sender_customer_id, 50)
        Account.add_balance(self.receiver_customer_id, 30)

    def testcase_transfer_balance(self):
        sender_old_balance = Account.get_balance(self.sender_customer_id)
        receiver_old_balance = Account.get_balance(self.receiver_customer_id)

        Account.transfer_balance(self.sender_customer_id,
                                 self.receiver_customer_id, 10)

        sender_new_balance = Account.get_balance(self.sender_customer_id)
        receiver_new_balance = Account.get_balance(self.receiver_customer_id)

        self.assertEquals(sender_old_balance, sender_new_balance+10)
        self.assertEquals(receiver_old_balance, receiver_new_balance-10)

    def testcase_transfer_more_than_sender_balance(self):
        with self.assertRaisesMessage(Exception, expected_message=
            'Sender Balance should be more than transfer amount'):
                Account.transfer_balance(
                    self.sender_customer_id, self.receiver_customer_id, 60)

    def testcase_transfer_balance_is_negative(self):
        with self.assertRaisesMessage(Exception, expected_message=
            'Transfer balance cannot be zero or negative'):
                Account.transfer_balance(
                    self.sender_customer_id, self.receiver_customer_id, -10)

        with self.assertRaisesMessage(Exception, expected_message=
            'Transfer balance cannot be zero or negative'):
                Account.transfer_balance(
                    self.sender_customer_id, self.receiver_customer_id, 0)

    def testcase_transfer_float_balance(self):
        with self.assertRaisesMessage(Exception, expected_message=
        'Transfer balance must be of type int'):
            Account.transfer_balance(
                self.sender_customer_id, self.receiver_customer_id, 10.5)

    def testcase_transfer_balance_for_non_existing_accounts(self):
        non_existent_sender_id = 'no_sender'
        non_existent_receiver_id = 'no_receiver'

        with self.assertRaisesMessage(Exception, 'Customer id doesnot exist'):
            Account.transfer_balance(
                non_existent_sender_id, non_existent_receiver_id, 10)

        with self.assertRaisesMessage(Exception, 'Customer id doesnot exist'):
            Account.transfer_balance(
                self.sender_customer_id, non_existent_receiver_id, 10)

        with self.assertRaisesMessage(Exception, 'Customer id doesnot exist'):
            Account.transfer_balance(
                non_existent_sender_id, self.receiver_customer_id, 10)

    def testcase_transfer_balance_between_same_account(self):
        with self.assertRaisesMessage(Exception, expected_message=
            'Cannot transfer balance between same account'):
                Account.transfer_balance(
                    self.sender_customer_id, self.sender_customer_id, 10)
