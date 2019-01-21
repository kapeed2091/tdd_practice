

REQUEST_BODY_JSON = """
{
    "debits": [
        {
            "amount": 1.1, 
            "customer_id": "string", 
            "transaction_description": "string", 
            "client_transaction_id": "string", 
            "client_info": "string"
        }
    ]
}
"""


RESPONSE_200_JSON = """
{
    "transactions": [
        {
            "client_transaction_id": "string", 
            "transaction_id": "string", 
            "transaction_status": "string"
        }
    ]
}
"""

