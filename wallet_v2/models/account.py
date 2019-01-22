from django.db import models


class Account(models.Model):
    CUSTOMER_ID_LENGTH = 20
    customer_id = models.CharField(max_length=CUSTOMER_ID_LENGTH)

    @classmethod
    def create_account(cls, customer_id):
        account = cls.objects.create(customer_id=customer_id)
        return {'customer_id': account.customer_id, 'account_id': ''}
