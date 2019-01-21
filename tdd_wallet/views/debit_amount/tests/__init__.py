# pylint: disable=wrong-import-position

APP_NAME = "tdd_wallet"
OPERATION_NAME = "debit_amount"
REQUEST_METHOD = "post"
URL_SUFFIX = "debit/v1/"

from .test_case_01 import TestCase01DebitAmountAPITestCase

__all__ = [
    "TestCase01DebitAmountAPITestCase"
]
