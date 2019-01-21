from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator
from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    request_data = kwargs['request_data']

    customer_ids = request_data['customer_ids']

    response = []
    for customer_id in customer_ids:
        if customer_id == 'string':
            response.append({
                "balance": 10,
                "customer_id": customer_id
            })
        elif customer_id == 'string1':
            response.append({
                "balance": 145,
                "customer_id": customer_id
            })

    return {"customers_balance": response}
