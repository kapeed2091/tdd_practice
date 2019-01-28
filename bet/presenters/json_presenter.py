"""
Created on 2019-01-28

@author: revanth
"""
from bet.presenters.base_presenter import Presenter


class JSONPresenter(Presenter):

    @classmethod
    def present_create_bet(cls, output_data):
        bet = output_data['bet']
        bet_participants = output_data['bet_participants']

        response = {
            'bet_id': bet['id'],
            'match_id': bet['match_id'],
            'amount': bet['amount'],
            'winner_id': bet['winner_id'],
            'participant_ids': [x['participant_id'] for x in bet_participants]
        }
        return response
