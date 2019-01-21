# pylint: disable=wrong-import-position

APP_NAME = "tdd_wallet"
OPERATION_NAME = "credit_amount"
REQUEST_METHOD = "post"
URL_SUFFIX = "credit/v1/"

from .test_case_01 import TestCase01CreditAmountAPITestCase

__all__ = [
    "TestCase01CreditAmountAPITestCase"
]
