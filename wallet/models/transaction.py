from django.db import models

class Transaction(models.Model):
    pass

    @classmethod
    def get_customer_statement(cls, customer_id):
        from wallet import entities
        return [entities.Transaction.create_credit_transaction(10)]