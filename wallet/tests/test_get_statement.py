from django.test import TestCase


class TestGetStatement(TestCase):
    customer_id = 'customer1'

    def test_get_customer_statement_for_user_without_transactions(self):
        from wallet.models import Transaction

        transactions = Transaction.get_statement(customer_id=self.customer_id)
        self.assertEqual(len(transactions), 0)
