from django import test

class TestGetCustomerStatement(test.TestCase):
    customer_id = 'customer1'

    def setUp(self):
        from wallet.models import Account
        account_details = Account.create_account(self.customer_id)
        self.account_id = account_details['account_id']
        Account.add_balance(self.customer_id, 10)
        from wallet import models
        self.transactions = models.Transaction.get_customer_statement(
            self.customer_id
        )
    def test_check_transaction_count(self):
        self.assertEqual(len(self.transactions), 1)

    def test_get_user_statement(self):
        from wallet import entities
        transaction_entity = entities.Transaction.create_credit_transaction(
            amount=10
        )
        self.assertEqual(self.transactions[0], transaction_entity)

    def test_check_transfer_type(self):
        from wallet import constants
        self.assertEqual(
            self.transactions[0].transfer_type,
            constants.TransferType.EXTERNAL.value
        )
