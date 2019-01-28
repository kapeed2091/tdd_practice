# Request-Response shouldn't be entities


class BetUseCase(object):
    def __init__(self, storage, presenter):
        self.storage = storage
        self.presenter = presenter

    def create_bet(self, request_data):
        bet_id = self.storage.create_bet(request_data)
        self.storage.create_bet_participant(bet_id,
                                            request_data['participant_ids'])
        self.presenter.convert(bet_id=bet_id)
        return

    def update_bet(self, match_id, winner_id):
        pass

    def get_bet_history(self, participant_id):
        pass

    def get_match_bet(self, match_id):
        pass
