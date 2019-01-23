from django.test import TestCase


class TestTransferAmount(TestCase):
    customer_id1 = 'customer1'
    customer_id2 = 'customer2'
    account_id1 = None
    account_id2 = None

    def setUp(self):
        from wallet.models import Account

        account_details1 = Account.create_account(self.customer_id1)
        self.account_id1 = account_details1['account_id']

        account_details2 = Account.create_account(self.customer_id2)
        self.account_id2 = account_details2['account_id']

    def testcase_transfer_amount(self):
        from wallet.models import Account
        transfer_amount = 10

        Account.add_balance(customer_id=self.customer_id1, amount=100)

        prev_customer_id1_balance = Account.get_balance(self.customer_id1)
        prev_customer_id2_balance = Account.get_balance(self.customer_id2)

        Account.transfer_amount(source_customer_id=self.customer_id1,
                                destination_customer_id=self.customer_id2,
                                transfer_amount=transfer_amount)

        customer_id1_balance = Account.get_balance(self.customer_id1)
        customer_id2_balance = Account.get_balance(self.customer_id2)

        self.assertEquals(customer_id1_balance,
                          prev_customer_id1_balance-transfer_amount)
        self.assertEquals(customer_id2_balance,
                          prev_customer_id2_balance + transfer_amount)

        self._validate_transaction_db_state(transfer_amount=transfer_amount)

    def test_case_transfer_negative_amount(self):
        from wallet.models import Account

        transfer_amount = -10

        with self.assertRaisesMessage(
                Exception,
                expected_message='Can not transfer the given amount'):
            Account.transfer_amount(source_customer_id=self.customer_id1,
                                    destination_customer_id=self.customer_id2,
                                    transfer_amount=transfer_amount)

    def test_case_transfer_zero_balance(self):
        from wallet.models import Account

        transfer_amount = 0

        with self.assertRaisesMessage(
                Exception,
                expected_message='Can not transfer the given amount'):
            Account.transfer_amount(source_customer_id=self.customer_id1,
                                    destination_customer_id=self.customer_id2,
                                    transfer_amount=transfer_amount)

    def test_case_transfer_float_balance(self):
        from wallet.models import Account

        transfer_amount = 0

        with self.assertRaisesMessage(
                Exception,
                expected_message='Can not transfer the given amount'):
            Account.transfer_amount(source_customer_id=self.customer_id1,
                                    destination_customer_id=self.customer_id2,
                                    transfer_amount=transfer_amount)

    def test_case_insufficient_balance_to_transfer(self):
        from wallet.models import Account

        transfer_amount = 200

        with self.assertRaisesMessage(
                Exception, expected_message=
                'Insufficient balance to make transfer'):
            Account.transfer_amount(source_customer_id=self.customer_id1,
                                    destination_customer_id=self.customer_id2,
                                    transfer_amount=transfer_amount)

    def test_case_invalid_receiver_account(self):
        from wallet.models import Account

        transfer_amount = 10
        Account.add_balance(customer_id=self.customer_id1, amount=100)

        with self.assertRaisesMessage(
                Exception, expected_message=
                'No account exists with the given customer id'):
            Account.transfer_amount(source_customer_id=self.customer_id1,
                                    destination_customer_id='customer3',
                                    transfer_amount=transfer_amount)

    def _validate_transaction_db_state(self, transfer_amount):
        from wallet.models import Transaction
        sender_transactions = \
            Transaction.objects.filter(account__customer_id=self.customer_id1)

        sender_transaction = sender_transactions[0]

        self.assertEquals(sender_transaction.account.customer_id, self.customer_id1)
        self.assertEquals(sender_transaction.amount, transfer_amount)
        self.assertEquals(sender_transaction.transaction_type, "DEBIT")

        receiver_transactions = \
            Transaction.objects.filter(account__customer_id=self.customer_id1)

        receiver_transaction = receiver_transactions[0]

        self.assertEquals(receiver_transaction.account.customer_id,
                          self.customer_id2)
        self.assertEquals(receiver_transaction.amount, transfer_amount)
        self.assertEquals(receiver_transaction.transaction_type, "CREDIT")
