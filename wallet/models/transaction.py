from django.db import models


class Transaction(models.Model):
    MESSAGE_LENGTH = 500
    TRANSACTION_TYPE_LENGTH = 20

    account = models.ForeignKey('wallet.Account')
    message = models.TextField(max_length=MESSAGE_LENGTH)
    amount = models.IntegerField()
    transaction_type = models.CharField(max_length=TRANSACTION_TYPE_LENGTH)

    def convert_transaction_to_dict(self):
        return {
            "customer_id": self.account.customer_id,
            "message": self.message,
            "amount": self.amount,
            "transaction_type": self.transaction_type
        }

    @classmethod
    def get_transactions(cls, customer_id):
        return cls.objects.filter(account__customer_id=customer_id)

    @classmethod
    def add_transaction(cls, transaction_dict):
        cls.objects.create(
            account_id=transaction_dict['account_id'],
            message=transaction_dict['message'],
            amount=transaction_dict['amount'],
            transaction_type=transaction_dict['transaction_type'])

    @classmethod
    def get_statement(cls, customer_id):
        transactions = cls.get_transactions(customer_id=customer_id)

        statement = []
        for transaction in transactions:
            statement.append(transaction.convert_transaction_to_dict())

        return statement

