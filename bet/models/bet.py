from django.db import models


class Bet(models.Model):
    match_id = models.IntegerField()
    amount = models.IntegerField()
    winner_id = models.IntegerField(default=-1)
