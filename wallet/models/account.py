from django.db import models


class Account(models.Model):
    CUSTOMER_ID_LENGTH = 20
    ACCOUNT_ID_LENGTH = 20
    DEFAULT_BALANCE = 0

    customer_id = models.CharField(max_length=CUSTOMER_ID_LENGTH, unique=True)
    account_id = models.CharField(max_length=ACCOUNT_ID_LENGTH, unique=True)
    balance = models.IntegerField(default=DEFAULT_BALANCE)

    @classmethod
    def create_account(cls, customer_id):
        return {'account_id': '', 'customer_id': ''}
