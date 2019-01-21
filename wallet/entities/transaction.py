class Transaction(object):
    def __init__(self, transaction_type, amount):
        self.transaction_type = transaction_type
        self.amount = amount

    @classmethod
    def create_credit_transaction(cls, amount):
        return cls(None, amount)

    def __eq__(self, other):
        return (self.transaction_type == other.transaction_type and
                self.amount == other.amount)


