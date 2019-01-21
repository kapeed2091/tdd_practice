from django.db import models


class Transaction(models.Model):
    account = models.ForeignKey('wallet.Account')
    amount = models.IntegerField()
    transaction_datetime = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_transaction_for_account_id(cls, account_id, amount):
        obj = cls(account_id=account_id, amount=amount)
        obj.save()
        return obj

    @classmethod
    def get_statement(cls, customer_id):
        return cls.objects.filter(
            account__customer_id=customer_id
        ).order_by('-transaction_datetime', '-id')

    def convert_to_dict(self):
        return {
            'transaction_id': self.id,
            'transaction_datetime': self.transaction_datetime,
            'amount': self.amount,
            'account_id': self.account_id
        }
