from enum import Enum

DEFAULT_DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class TransactionType(Enum):
    CREDIT = 'CREDIT'
    DEBIT = 'DEBIT'
