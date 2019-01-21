from enum import Enum
from ib_common.constants import BaseEnumClass


class TransactionType(BaseEnumClass, Enum):
    ADD_BALANCE = "ADD_BALANCE"
    MONEY_CREDITED = "MONEY_CREDITED"
    MONEY_DEBITED = "MONEY_DEBITED"
