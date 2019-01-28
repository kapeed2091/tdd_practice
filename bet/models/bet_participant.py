from django.db import models


class BetParticipant(models.Model):
    bet_id = models.IntegerField()
    participant_id = models.IntegerField()