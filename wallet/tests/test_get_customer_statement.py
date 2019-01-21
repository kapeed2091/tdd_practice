from django import test

class TestGetCustomerStatement(test.TestCase):
    customer_id = 'customer1'

    def setUp(self):
        from wallet.models import Account
        account_details = Account.create_account(self.customer_id)
        self.account_id = account_details['account_id']
        Account.add_balance(self.customer_id, 10)

    def test_get_user_statement(self):
        from wallet import models, entities
        transactions = models.Transaction.get_customer_statement(self.customer_id)
        self.assertEqual(len(transactions), 1)
        transaction_entity = entities.Transaction.create_credit_transaction(amount=10)
        self.assertEqual(transactions[0], transaction_entity)