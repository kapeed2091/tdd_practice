from django.db import models


class BetParticipant(models.Model):
    bet = models.ForeignKey('bet.Bet')
    participant_id = models.IntegerField()

    def to_dict(self):
        return {
            'id': self.id,
            'bet_id': self.bet_id,
            'participant_id': self.participant_id
        }
