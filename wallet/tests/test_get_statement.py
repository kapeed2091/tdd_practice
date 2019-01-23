"""
Created on 2019-01-23

@author: revanth
"""
from django.test import TestCase


class TestGetStatement(TestCase):
    customer_id = 'Customer1'

    def test_get_statement(self):
        from wallet.models import Transaction
        statement = Transaction.get_statement(self.customer_id)
        self.assertEquals(statement['total'], 0)
        self.assertEquals(statement['transactions'], [])
