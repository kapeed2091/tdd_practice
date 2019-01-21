from django.db import models

from wallet.constants.general import TransactionType


class Transaction(models.Model):
    CUSTOMER_ID_LENGTH = 20
    TRANSACTION_TYPE_LENGTH = 20

    customer_id = models.CharField(max_length=CUSTOMER_ID_LENGTH)
    transaction_type = models.CharField(max_length=TRANSACTION_TYPE_LENGTH,
                                        choices=TransactionType.get_list_of_tuples())
    transaction_money = models.IntegerField()

    @classmethod
    def get_statement(cls, customer_id):
        return []
