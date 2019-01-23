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

    def testcase_get_statement_with_single_transaction(self):
        Account.add_balance(self.sender_customer_id, 50)
        Account.add_balance(self.receiver_customer_id, 30)
        transaction_id = '2019_1'

        from wallet.models import Transaction
        Transaction.assign_transaction_id(customer_id=self.sender_customer_id,
                                          transaction_id=transaction_id,
                                          amount=50)

        sender_transactions_list = Transaction.get_statement(
            self.sender_customer_id)

        self.assertEquals(sender_transactions_list,
                          [{'customer_id': self.sender_customer_id,
                            'transaction_id': transaction_id, 'amount': 50}])

    def testcase_unique_transaction_id(self):
        Account.add_balance(self.sender_customer_id, 50)
        Account.add_balance(self.receiver_customer_id, 30)
        transaction_id = '2019_1'

        from wallet.models import Transaction
        Transaction.assign_transaction_id(customer_id=self.sender_customer_id,
                                          transaction_id=transaction_id,
                                          amount=50)

        Account.add_balance(self.sender_customer_id, 20)
        with self.assertRaises(Exception):
            Transaction.assign_transaction_id(
                customer_id=self.sender_customer_id,
                transaction_id=transaction_id, amount=20)
