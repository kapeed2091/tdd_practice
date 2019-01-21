# pylint: disable=wrong-import-position

APP_NAME = "tdd_wallet"
OPERATION_NAME = "get_wallet_balance"
REQUEST_METHOD = "post"
URL_SUFFIX = "balance/v1/"

from .test_case_01 import TestCase01GetWalletBalanceAPITestCase
from .test_case_02 import TestCase02GetWalletBalanceAPITestCase

__all__ = [
    "TestCase01GetWalletBalanceAPITestCase",
    "TestCase02GetWalletBalanceAPITestCase"
]
