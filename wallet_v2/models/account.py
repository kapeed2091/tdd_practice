from django.db import models


class Account(models.Model):
    pass

    @classmethod
    def create_account(cls, customer_id):
        return {'customer_id': '', 'account_id': ''}
