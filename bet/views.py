

def validate_amount(amount):
    if type(amount) != int or amount <= 0:
        raise Exception


def validate_participant_ids(participant_ids):
    for p_id in participant_ids:
        if type(p_id) != int or p_id <= 0:
            raise Exception


def validate_match_id(match_id):
    if type(match_id) != int or match_id <= 0:
        raise Exception


def create_bet(**kwargs):
    request_data = kwargs['request_data']

    validate_match_id(match_id=request_data['match_id'])
    validate_participant_ids(participant_ids=request_data['participant_ids'])
    validate_amount(amount=request_data['amount'])

    from bet.storages.rdb_storage import RDBStorage
    storage = RDBStorage()

    from bet.presenters.json_presenter import JSONPresenter
    presenter = JSONPresenter()

    from bet.usecases import BetUseCase
    bet_usecase = BetUseCase(storage=storage, presenter=presenter)
    response = bet_usecase.create_bet(request_data=request_data)

    return response
