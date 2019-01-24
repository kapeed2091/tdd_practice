from django.db import models


class Transaction(models.Model):
    TRANSACTION_TYPE_LENGTH = 10

    account = models.ForeignKey('wallet_v2.Account')
    amount = models.IntegerField()
    transaction_type = models.CharField(max_length=TRANSACTION_TYPE_LENGTH)
    transaction_date = models.DateTimeField()

    @classmethod
    def create_transaction(cls, transaction_details):
        """
        :param transaction_details:
        {
            'account_id': 1,
            'amount': 100,
            'transaction_type': 'CREDIT',
            'transaction_date': date_time object
        }
        :return:
        """
        cls.objects.create(
            account_id=transaction_details['account_id'],
            amount=transaction_details['amount'],
            transaction_type=transaction_details['transaction_type'],
            transaction_date=transaction_details['transaction_date'])
        return

    @classmethod
    def get_statement(cls, customer_id):
        from wallet_v2.models import Account
        account = Account.get_account(customer_id)
        transactions = cls.query_transactions_with_account_id(account.id)
        return cls.get_transaction_details(transactions)

    @classmethod
    def get_statement_within_date_range(
            cls, customer_id, from_date_str, to_date_str):
        from wallet_v2.models import Account

        from_date, to_date = cls.get_from_and_to_datetime_objects(
            from_date_str, to_date_str)
        account = Account.get_account(customer_id)
        transactions = cls.query_account_transactions_within_date_range(
            account.id, from_date, to_date)
        return cls.get_transaction_details_with_date(transactions)

    @classmethod
    def query_transactions_with_account_id(cls, account_id):
        return cls.objects.filter(account_id=account_id)

    @classmethod
    def get_transaction_details(cls, transactions):
        return [
            {
                'amount': transaction.amount,
                'transaction_type': transaction.transaction_type
            } for transaction in transactions
        ]

    @classmethod
    def query_account_transactions_within_date_range(
            cls, account_id, from_date, to_date):
        return cls.objects.filter(
            account_id=account_id,
            transaction_date__gte=from_date, transaction_date__lte=to_date)

    @classmethod
    def get_from_and_to_datetime_objects(cls, from_date_str, to_date_str):
        from ib_common.date_time_utils.convert_string_to_local_date_time \
            import convert_string_to_local_date_time
        from wallet_v2.constants.general import DEFAULT_DATE_TIME_FORMAT

        from_date = convert_string_to_local_date_time(
            from_date_str, DEFAULT_DATE_TIME_FORMAT)
        to_date = convert_string_to_local_date_time(
            to_date_str, DEFAULT_DATE_TIME_FORMAT)
        return from_date, to_date

    @classmethod
    def get_transaction_details_with_date(cls, transactions):
        from ib_common.date_time_utils.convert_datetime_to_local_string import \
            convert_datetime_to_local_string
        from wallet_v2.constants.general import DEFAULT_DATE_TIME_FORMAT

        return [
            {
                'amount': transaction.amount,
                'transaction_type': transaction.transaction_type,
                'date': convert_datetime_to_local_string(
                    transaction.transaction_date, DEFAULT_DATE_TIME_FORMAT)
            } for transaction in transactions
        ]
