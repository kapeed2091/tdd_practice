class CreateBetOutputPort(object):
    def convert(self, *args, **kwargs):
        raise NotImplementedError


class CreateBetUseCasePresenter(CreateBetOutputPort):
    def convert(self, *args, **kwargs):
        return {'bet_id': kwargs['bet_id']}
