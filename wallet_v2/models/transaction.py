from django.db import models


class Transaction(models.Model):
    TRANSACTION_TYPE_LENGTH = 10

    account = models.ForeignKey('wallet_v2.Account')
    amount = models.IntegerField()
    transaction_type = models.CharField(max_length=TRANSACTION_TYPE_LENGTH)
    transaction_date = models.DateTimeField()

    @classmethod
    def get_customer_statement(cls, customer_id):
        customer_transactions = cls.objects.filter(
            account__customer_id=customer_id)
        return [
            {
                'amount': transaction.amount,
                'transaction_type': transaction.transaction_type
            } for transaction in customer_transactions
        ]

    @classmethod
    def get_customer_statement_within_date_range(
            cls, customer_id, from_date_str, to_date_str):
        from ib_common.date_time_utils.convert_string_to_local_date_time \
            import convert_string_to_local_date_time
        from ib_common.date_time_utils.convert_datetime_to_local_string import \
            convert_datetime_to_local_string
        from wallet_v2.constants.general import DEFAULT_DATE_TIME_FORMAT

        from_date = convert_string_to_local_date_time(
            from_date_str, DEFAULT_DATE_TIME_FORMAT)
        to_date = convert_string_to_local_date_time(
            to_date_str, DEFAULT_DATE_TIME_FORMAT)

        customer_transactions = cls.objects.filter(
            account__customer_id=customer_id,
            transaction_date__gte=from_date, transaction_date__lte=to_date)
        return [
            {
                'amount': transaction.amount,
                'transaction_type': transaction.transaction_type,
                'date': convert_datetime_to_local_string(
                    transaction.transaction_date, DEFAULT_DATE_TIME_FORMAT)
            } for transaction in customer_transactions
        ]
