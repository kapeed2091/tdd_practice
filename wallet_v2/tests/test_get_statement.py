from django.test import TestCase

customer_1_transactions = [
    {
        'amount': 100,
        'transaction_type': 'CREDIT'
    },
    {
        'amount': 10,
        'transaction_type': 'DEBIT'
    }
]

customer_2_transactions = [
    {
        'amount': 10,
        'transaction_type': 'CREDIT'
    },
    {
        'amount': 10,
        'transaction_type': 'DEBIT'
    }
]


class TestGetStatement(TestCase):
    customer_id_1 = 'customer1'
    customer_id_2 = 'customer2'

    @staticmethod
    def create_transactions(transactions_list):
        from wallet_v2.models import Transaction

        for transaction in transactions_list:
            Transaction.objects.create(
                amount=transaction['amount'],
                transaction_type=transaction['transaction_type'])

    def testcase_get_customer_statement(self):
        from wallet_v2.models import Account, Transaction

        Account.create_account(self.customer_id_1)
        self.create_transactions(customer_1_transactions)
        self.create_transactions(customer_2_transactions)

        customer_transactions = Transaction.get_customer_statement(
            self.customer_id_1)
        self.assertItemsEqual(customer_transactions, customer_1_transactions)
