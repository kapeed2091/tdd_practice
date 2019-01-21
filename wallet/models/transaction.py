from django.db import models


class Transaction(models.Model):
    account = models.ForeignKey('wallet.Account')
    amount = models.IntegerField()

    @classmethod
    def get_statement(cls, customer_id):
        return cls.objects.filter(account__customer_id=customer_id)
