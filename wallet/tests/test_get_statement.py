from django.test import TestCase


class TestGetStatement(TestCase):
    customer_id = 'customer1'
    amount = 100

    def setUp(self):
        from wallet.models import Account

        account_details1 = Account.create_account(self.customer_id)
        self.account_id1 = account_details1['account_id']

        Account.add_balance(customer_id=self.customer_id, amount=self.amount)

    def test_case_get_statement(self):
        from wallet.models.transaction import Transaction

        transactions = Transaction.\
            get_statement(customer_id=self.customer_id)
        transaction = transactions[0]

        self.assertEquals(transaction['amount'], self.amount)
        self.assertEquals(transaction['customer_id'], self.customer_id)
        self.assertEquals(transaction['transaction_type'], "CREDIT")

    def test_case_invalid_customer_id(self):
        from wallet.models.transaction import Transaction

        with self.assertRaisesMessage(
                Exception, expected_message=
                'No account exists with the given customer id'):
            Transaction.get_statement(customer_id="customer3")
