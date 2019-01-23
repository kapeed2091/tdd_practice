"""
Created on 2019-01-23

@author: revanth
"""
from django.db import models


class Transaction(models.Model):

    @classmethod
    def get_statement(cls, customer_id):
        return {
            'total': 0,
            'transactions': []
        }
