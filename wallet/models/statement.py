from django.db import models


class Statement(models.Model):
    pass

    @classmethod
    def add_transactions(cls, transactions):
        pass

    @classmethod
    def get_transactions(cls, date_range):
        pass
