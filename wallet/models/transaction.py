from django.db import models


class Transaction(models.Model):

    @classmethod
    def get_statement(cls, customer_id):
        return []
