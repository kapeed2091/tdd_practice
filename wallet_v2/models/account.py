from django.db import models


class Account(models.Model):
    CUSTOMER_ID_LENGTH = 20
    ACCOUNT_ID_LENGTH = 20
    customer_id = models.CharField(max_length=CUSTOMER_ID_LENGTH, unique=True)
    account_id = models.CharField(max_length=ACCOUNT_ID_LENGTH, unique=True)

    @classmethod
    def create_account(cls, customer_id):
        try:
            cls.objects.get(customer_id=customer_id)
            raise Exception
        except cls.DoesNotExist:
            account_id = cls.generate_account_id(cls.ACCOUNT_ID_LENGTH)
            account = cls.assign_account(customer_id, account_id)
        return {'customer_id': account.customer_id,
                'account_id': account.account_id}

    @staticmethod
    def generate_account_id(length):
        import uuid
        return str(uuid.uuid4())[: length]

    @classmethod
    def assign_account(cls, customer_id, account_id):
        return cls.objects.create(customer_id=customer_id,
                                  account_id=account_id)
