from django.test import TestCase


class TestGetStatement(TestCase):
    customer_id_1 = 'customer1'

    def setUp(self):
        from wallet.models import Account, Transaction

        Account.create_account(self.customer_id_1)
        account = Account.get_account(self.customer_id_1)
        Transaction.create_obj(account=account, amount=10)
        Transaction.create_obj(account=account, amount=-10)

    def testcase_get_transactions(self):
        from wallet.models import Transaction

        transactions = Transaction.get_transactions(self.customer_id_1)
        self.assertEqual(len(transactions), 2)
        expected_transactions = [
            {'customer_id': 'customer1', 'amount': 10},
            {'customer_id': 'customer1', 'amount': -10}
        ]
        self.assertItemsEqual(expected_transactions, transactions)
