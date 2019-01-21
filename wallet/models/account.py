from django.db import models


class Account(models.Model):
    customer_id = models.CharField(max_length=20)
    account_id = models.CharField(max_length=20)

    @staticmethod
    def create_account(customer_id):
        account = Account.objects.create(customer_id=customer_id)
        # account.account_id = 
        return {'customer_id': customer_id, 'account_id': account.account_id}
        