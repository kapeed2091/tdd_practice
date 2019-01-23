from django.test import TestCase
from wallet.models import Account


class TestGetStatement(TestCase):
    sender_customer_id = 'sender'
    receiver_customer_id = 'receiver'

    def setUp(self):
        Account.create_and_return_account(self.sender_customer_id)
        Account.create_and_return_account(self.receiver_customer_id)

    def testcase_get_statement(self):
        from wallet.models import Transaction
        transactions_list = Transaction.get_statement(self.sender_customer_id)

        self.assertEquals(transactions_list, [])

    def testcase_get_statement_with_single_transaction(self):
        transaction_id = '2019_1'

        from wallet.models import Transaction
        Transaction.assign_transaction_id(customer_id=self.sender_customer_id,
                                          transaction_id=transaction_id,
                                          amount=50, type='Credit')

        sender_transactions_list = Transaction.get_statement(
            self.sender_customer_id)

        self.assertEquals(sender_transactions_list,
                          [{'customer_id': self.sender_customer_id,
                            'transaction_id': transaction_id, 'amount': 50,
                            'type': 'Credit'}])

    def testcase_unique_transaction_id(self):
        transaction_id = '2019_1'

        from wallet.models import Transaction
        Transaction.assign_transaction_id(customer_id=self.sender_customer_id,
                                          transaction_id=transaction_id,
                                          amount=50, type='Credit')

        with self.assertRaises(Exception):
            Transaction.assign_transaction_id(
                customer_id=self.sender_customer_id,
                transaction_id=transaction_id, amount=20, type='Credit')

    def testcase_get_transaction_type_in_statement(self):
        transaction_id_1 = '2019_1'
        transaction_id_2 = '2019_2'

        from wallet.models import Transaction
        Transaction.assign_transaction_id(customer_id=self.sender_customer_id,
                                          transaction_id=transaction_id_1,
                                          amount=50, type='Credit')

        old_sender_transactions_list = Transaction.get_statement(
            self.sender_customer_id)
        self.assertEquals(old_sender_transactions_list, [{
            'customer_id': self.sender_customer_id,
            'transaction_id': transaction_id_1,
            'amount': 50, 'type': 'Credit'}])

        Transaction.assign_transaction_id(customer_id=self.sender_customer_id,
                                          transaction_id=transaction_id_2,
                                          amount=10, type='Debit')

        new_sender_transactions_list = Transaction.get_statement(
            self.sender_customer_id)
        self.assertEquals(new_sender_transactions_list, [{
            'customer_id': self.sender_customer_id,
            'transaction_id': transaction_id_1,
            'amount': 50, 'type': 'Credit'},
            {'customer_id': self.sender_customer_id,
             'transaction_id': transaction_id_2,
             'amount': 10, 'type': 'Debit'}])
