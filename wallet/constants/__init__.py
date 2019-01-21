import enum

class TransferType(enum.Enum):
    EXTERNAL = 'EXTERNAL'
    INTERNAL = 'INTERNAL'

class TransactionType(enum.Enum):
    CREDIT = 'CREDIT'
    DEBIT = 'DEBIT'
