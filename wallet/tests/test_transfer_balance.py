from django.test import TestCase


class TestTransferBalance(TestCase):
    customer_id_1 = 'customer1'
    customer_id_2 = 'customer2'
    invalid_customer_id = 'customer3'

    def setUp(self):
        from wallet.models import Account
        Account.create_account(self.customer_id_1)
        customer1_account = Account.get_account(self.customer_id_1)
        customer1_account.add_balance(amount=100)
        Account.create_account(self.customer_id_2)
        customer2_account = Account.get_account(self.customer_id_2)
        customer2_account.add_balance(amount=10)

    def testcase_transfer_positive_amount(self):
        from wallet.models import Account
        Account.transfer_amount(sender_id=self.customer_id_1,
                                receiver_id=self.customer_id_2, amount=50)
        customer_1_balance = Account.get_balance(self.customer_id_1)
        customer_2_balance = Account.get_balance(self.customer_id_2)
        self.assertEqual(customer_1_balance, 50)
        self.assertEqual(customer_2_balance, 60)

    def testcase_transfer_negative_amount(self):
        from wallet.models import Account

        with self.assertRaisesMessage(Exception, expected_message='Invalid amount'):
            Account.transfer_amount(sender_id=self.customer_id_1,
                                    receiver_id=self.customer_id_2, amount=-50)
        customer_1_balance = Account.get_balance(self.customer_id_1)
        customer_2_balance = Account.get_balance(self.customer_id_2)
        self.assertEqual(customer_1_balance, 100)
        self.assertEqual(customer_2_balance, 10)

    def testcase_transfer_zero_amount(self):
        from wallet.models import Account

        with self.assertRaisesMessage(Exception, expected_message='Invalid amount'):
            Account.transfer_amount(sender_id=self.customer_id_1,
                                    receiver_id=self.customer_id_2, amount=0)
        customer_1_balance = Account.get_balance(self.customer_id_1)
        customer_2_balance = Account.get_balance(self.customer_id_2)
        self.assertEqual(customer_1_balance, 100)
        self.assertEqual(customer_2_balance, 10)

    def testcase_transfer_insufficient_account(self):
        from wallet.models import Account

        with self.assertRaisesMessage(Exception, expected_message='Insufficient balance'):
            Account.transfer_amount(sender_id=self.customer_id_1,
                                    receiver_id=self.customer_id_2, amount=500)
        customer_1_balance = Account.get_balance(self.customer_id_1)
        customer_2_balance = Account.get_balance(self.customer_id_2)
        self.assertEqual(customer_1_balance, 100)
        self.assertEqual(customer_2_balance, 10)

    def testcase_invalid_sender_id(self):
        from wallet.models import Account

        with self.assertRaisesMessage(Exception, expected_message='Invalid sender id'):
            Account.transfer_amount(sender_id=self.invalid_customer_id,
                                    receiver_id=self.customer_id_2, amount=50)
        customer_1_balance = Account.get_balance(self.customer_id_1)
        customer_2_balance = Account.get_balance(self.customer_id_2)
        self.assertEqual(customer_1_balance, 100)
        self.assertEqual(customer_2_balance, 10)

    def testcase_invalid_receiver_id(self):
        from wallet.models import Account

        with self.assertRaisesMessage(Exception, expected_message='Invalid receiver id'):
            Account.transfer_amount(sender_id=self.customer_id_1,
                                    receiver_id=self.invalid_customer_id, amount=50)
        customer_1_balance = Account.get_balance(self.customer_id_1)
        customer_2_balance = Account.get_balance(self.customer_id_2)
        self.assertEqual(customer_1_balance, 100)
        self.assertEqual(customer_2_balance, 10)

    def testcase_transfer_amount_and_check_transaction_entry(self):
        from wallet.models import Account, Transaction
        Account.transfer_amount(sender_id=self.customer_id_1,
                                receiver_id=self.customer_id_2, amount=50)
        customer1_transactions = Transaction.get_transactions(self.customer_id_1)
        self.assertEqual(len(customer1_transactions), 2)
        expected_customer1_transactions = [
            {'customer_id': self.customer_id_1, 'amount': 100},
            {'customer_id': self.customer_id_1, 'amount': -50}
        ]
        self.assertItemsEqual(expected_customer1_transactions, customer1_transactions)

        customer2_transactions = Transaction.get_transactions(self.customer_id_2)
        self.assertEqual(len(customer2_transactions), 2)
        expected_customer2_transactions = [
            {'customer_id': self.customer_id_2, 'amount': 10},
            {'customer_id': self.customer_id_2, 'amount': 50}
        ]
        self.assertItemsEqual(expected_customer2_transactions, customer2_transactions)
