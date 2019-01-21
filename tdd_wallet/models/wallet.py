from django.db import models


class Wallet(models.Model):
    customer_id = models.CharField(max_length=100)
    balance = models.FloatField()
    pass
