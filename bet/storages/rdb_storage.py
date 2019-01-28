from bet.storages.base_storage import Storage
from bet import models

# TODO-Doubt: what should be input-output parameters for storage?


class RDBStorage(Storage):
    def create_bet(self, bet):
        match_id = bet['match_id']
        amount = bet['amount']
        bet = models.Bet.objects.create(match_id=match_id, amount=amount)
        return bet.id

    def create_bet_participant(self, bet_id, participant_ids):
        to_create = []
        for p_id in participant_ids:
            to_create.append(models.BetParticipant(bet_id=bet_id,
                                                   participant_id=p_id))
        models.BetParticipant.objects.bulk_create(to_create)
        return
