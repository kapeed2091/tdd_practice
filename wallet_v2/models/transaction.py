from django.db import models


class Transaction(models.Model):
    TRANSACTION_TYPE_LENGTH = 10

    account = models.ForeignKey('wallet_v2.Account')
    amount = models.IntegerField()
    transaction_type = models.CharField(max_length=TRANSACTION_TYPE_LENGTH)
    transaction_date = models.DateField()

    @classmethod
    def get_customer_statement(cls, customer_id):
        customer_transactions = cls.objects.filter(
            account__customer_id=customer_id)
        return [
            {
                'amount': transaction.amount,
                'transaction_type': transaction.transaction_type
            } for transaction in customer_transactions
        ]

    @classmethod
    def get_customer_statement_within_date_range(
            cls, customer_id, from_date_str, to_date_str):
        return []
