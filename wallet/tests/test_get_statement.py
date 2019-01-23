"""
Created on 2019-01-23

@author: revanth
"""
from django.test import TestCase


class TestGetStatement(TestCase):
    customer_id = 'Customer1'

    def test_get_statement_no_transactions(self):
        from wallet.models import Transaction
        statement = Transaction.get_statement(self.customer_id)
        self.assertEquals(statement['total'], 0)
        self.assertEquals(statement['transactions'], [])

    def test_get_statement_with_one_transaction(self):
        from wallet.models import Transaction
        from datetime import datetime
        Transaction.objects.create(
            transaction_id='abcd', date=datetime.today(), amount=100,
            balance=100, transaction_type='CREDIT')
        statement = Transaction.get_statement(self.customer_id)
        self.assertEquals(statement['total'], 1)
        self.assertEquals(statement['transactions'], [{
            'transaction_id': 'abcd',
            'date': datetime.now().strftime("%Y-%m-%d"),
            'amount': 100,
            'balance': 100,
            'transaction_type': 'CREDIT'
        }])

