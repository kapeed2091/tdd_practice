from wallet import constants

class Transaction(object):
    def __init__(self, transaction_type, transfer_type, amount):
        self.transaction_type = transaction_type
        self.transfer_type = transfer_type
        self.amount = amount

    @classmethod
    def create_credit_transaction(cls, amount):
        return cls(
            transaction_type=constants.TransactionType.CREDIT.value,
            transfer_type=constants.TransferType.EXTERNAL.value,
            amount=amount
        )

    def __eq__(self, other):
        return (
            self.transaction_type == other.transaction_type and
            self.transfer_type == other.transfer_type and
            self.amount == other.amount
        )
