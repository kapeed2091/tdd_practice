from django.test import TestCase


class TestGetStatement(TestCase):
    customer_id = 'customer1'

    TRANSACTIONS_DICT = [
        {
            'account_id': 1,
            'amount': 1
        },
        {
            'account_id': 1,
            'amount': 2
        }
    ]

    def create_account(self):
        from wallet.models import Account
        Account.create_account(customer_id=self.customer_id)

    def create_transactions(self):
        import copy
        from wallet.models import Transaction

        for item in copy.deepcopy(self.TRANSACTIONS_DICT):
            Transaction.create_transaction_for_account_id(
                account_id=item['account_id'],
                amount=item['amount']
            )

    def test_get_customer_statement_for_user_without_transactions(self):
        from wallet.models import Transaction

        transactions = Transaction.get_statement(customer_id=self.customer_id)
        self.assertEqual(len(transactions), 0)

    def test_get_statement_for_user_with_transactions(self):
        from wallet.models import Transaction

        self.create_account()
        self.create_transactions()

        transactions = Transaction.get_statement(customer_id=self.customer_id)
        self.assertEqual(len(transactions), 2)
