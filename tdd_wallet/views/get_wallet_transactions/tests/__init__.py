# pylint: disable=wrong-import-position

APP_NAME = "tdd_wallet"
OPERATION_NAME = "get_wallet_transactions"
REQUEST_METHOD = "post"
URL_SUFFIX = "wallets/transactions/v1/"

from .test_case_01 import TestCase01GetWalletTransactionsAPITestCase

__all__ = [
    "TestCase01GetWalletTransactionsAPITestCase"
]
