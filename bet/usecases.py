# Request-Response shouldn't be entities


class BetUseCase(object):
    def __init__(self, storage, presenter):
        self.storage = storage
        self.presenter = presenter

    def create_bet(self, request_data):

        bet_id = self.storage.create_bet(request_data)
        self.storage.create_bet_participants(
            bet_id, request_data['participant_ids'])

        # TODO doubt: will the below get logic be in usecase layer or presenter layer ?

        bet = self.storage.get_bet(bet_id)
        bet_participants = self.storage.get_bet_participants(bet_id)

        output_data = {
            'bet': bet,
            'bet_participants': bet_participants
        }
        return self.presenter.present_create_bet(output_data)

    def update_bet(self, match_id, winner_id):
        pass

    def get_bet_history(self, participant_id):
        pass

    def get_match_bet(self, match_id):
        pass
