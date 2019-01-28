class PublicIP(object):
    def __init__(self, usecase):

    def create_bet(self, match_id, participant_ids, amount):
        request_object = {
            'match_id': match_id,
            'participant_ids': participant_ids,
            'amount': amount
        }



class AbstractPublicIP():
    def create_bet(self):
        raise NotImplementedError