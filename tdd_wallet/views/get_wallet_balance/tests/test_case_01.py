import mock

from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import \
    CustomAPITestCase
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

request_body = """
{
    "customer_ids": [
        "string"
    ]
}
"""
"""
to test balance
"""
response_body = """
{
    "customers_balance": [
        {
            "balance": 10, 
            "customer_id": "string"
        }
    ]
}
"""

test_case = {
    "request": {
        "path_params": {},
        "query_params": {},
        "header_params": {
            "API_GATEWAY_AUTHORIZER": {
                "claims": {
                    "cognito:username": "TEST-1"
                }
            }
        },
        "securities": {"JWTToken": {"header_name": "HTTP_AUTHORIZATION", "type": "apiKey", "name": "Authorization", "value": "api_key", "in": "header"}},
        "body": request_body,
    },
    "response": {
        "status": 200,
        "body": response_body,
        "header_params": {}
    }
}


class TestCase01GetWalletBalanceAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01GetWalletBalanceAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    def test_case(self):
        super(TestCase01GetWalletBalanceAPITestCase, self).test_case()
