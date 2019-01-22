from django.test import TestCase


class TestGetStatement(TestCase):
    customer_id = 'customer1'

    def setUp(self):
        from wallet.models import Account

        account_details1 = Account.create_account(self.customer_id)
        self.account_id1 = account_details1['account_id']

        Account.add_balance(customer_id=self.customer_id, amount=100)

    def test_case_get_statement(self):

        Transaction.get_statement(customer_id=self.customer_id)

