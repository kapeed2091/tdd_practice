from bet.storages.base_storage import Storage
from bet import models

# TODO-Doubt: what should be input-output parameters for storage?
# TODO: Every exception django raises should have an equivalent exception
# TODO-Doubt: will the implementations be in this file or will they be the in the model file?


class RDBStorage(Storage):

    @classmethod
    def create_bet(cls, bet):
        match_id = bet['match_id']
        amount = bet['amount']
        bet = models.Bet.objects.create(match_id=match_id, amount=amount)
        return bet.id

    @classmethod
    def create_bet_participants(cls, bet_id, participant_ids):
        to_create = []
        for p_id in participant_ids:
            to_create.append(models.BetParticipant(bet_id=bet_id,
                                                   participant_id=p_id))
        models.BetParticipant.objects.bulk_create(to_create)
        return

    @classmethod
    def get_bet(cls, bet_id):
        return models.Bet.objects.get(id=bet_id).to_dict()

    @classmethod
    def get_bet_participants(cls, bet_id):
        bet_participants = models.Bet.objects.filter(bet_id=bet_id)
        return [x.to_dict() for x in bet_participants]
