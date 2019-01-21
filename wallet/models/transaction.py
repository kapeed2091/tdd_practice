from django.db import models

class Transaction(models.Model):
    pass

    @classmethod
    def get_customer_statement(cls, customer_id):
        return [1]