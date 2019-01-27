from django.db import models
from wallet import entities


class Transaction(models.Model):
    account = models.ForeignKey('account')
    amount = models.IntegerField(default=0)

    @classmethod
    def create_transaction(cls, account, amount):
        cls.objects.create(
            account=account,
            amount=amount
        )

    def to_entity(self):
        return entities.Transaction(
            id=self.id, account_id=self.account_id, amount=self.amount)

    @classmethod
    def get_transactions(cls, customer_id):
        from wallet.models import Account

        try:
            account = Account.get_account(customer_id)
            transactions = cls.objects.filter(account=account)
            return [each.convert_to_dict() for each in transactions]
        except Account.DoesNotExist:
            raise Exception('Invalid Customer Id')

    def convert_to_dict(self):
        return {
            'customer_id': self.account.customer_id,
            'amount': self.amount
        }
