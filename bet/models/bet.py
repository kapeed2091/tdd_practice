from django.db import models


class Bet(models.Model):
    match_id = models.IntegerField()
    amount = models.IntegerField()
    winner_id = models.IntegerField(default=-1)

    def to_dict(self):
        return {
            'id': self.id,
            'match_id': self.match_id,
            'amount': self.amount,
            'winner_id': self.winner_id
        }
