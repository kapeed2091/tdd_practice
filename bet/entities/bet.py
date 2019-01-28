class Bet(object):
    def __init__(self, match_id, participant_ids, amount, winner_id):
        self.match_id = match_id
        self.participant_ids = participant_ids
        self.amount = amount
        self.winner_id = winner_id
