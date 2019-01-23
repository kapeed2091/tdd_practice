from django.test import TestCase


class TestGetStatement(TestCase):
    customer_id = 'customer1'
    no_transactions_customer_id = 'customer3'
    transactions = [
        {
            "date_time": "2017-12-12 13:00:00",
            "amount": 100,
            "status": "DEBIT",
            "customer_id": 'customer1'
        },
        {
            "date_time": "2017-12-13 13:00:00",
            "amount": 110,
            "status": "CREDIT",
            "customer_id": 'customer1'
        },
        {
            "date_time": "2017-12-14 13:00:00",
            "amount": 120,
            "status": "DEBIT",
            "customer_id": 'customer2'
        },
        {
            "date_time": "2017-12-15 13:00:00",
            "amount": 130,
            "status": "CREDIT",
            "customer_id": 'customer2'
        },
        {
            "date_time": "2017-12-18 13:00:00",
            "amount": 130,
            "status": "CREDIT",
            "customer_id": 'customer3'
        }
    ]

    def setup_statements_for_both_customers(self):
        from wallet.models import Statement
        for each in self.transactions:
            Statement.objects.create(
                date_time=each.get("date_time"),
                amount=each.get("amount"),
                status=each.get("status"),
                customer_id=each["customer_id"]
            )

    def _get_customer_transactions(self, date_range, customer_id):
        transactions = []
        for each in self.transactions:
            if date_range["from_date"] <= each["date_time"] <= date_range[
                    "to_date"] and each["customer_id"] == customer_id:
                transactions.append(each)

        return transactions

    @staticmethod
    def _get_parsed_date_range(date_range):
        from ib_common.date_time_utils.convert_string_to_local_date_time \
            import convert_string_to_local_date_time

        date_time_format = '%Y-%m-%d %H:%M:%S'

        date_range = {
            "from_date": convert_string_to_local_date_time(
                date_range["from_date"], date_time_format
            ),
            "to_date": convert_string_to_local_date_time(
                date_range["to_date"], date_time_format
            )
        }

        return date_range

    def test_get_balance_successful(self):
        self.setup_statements_for_both_customers()

        from wallet.models import Statement

        from_date = "2017-12-12 13:00:00"
        to_date = "2017-12-16 13:00:00"

        from ib_common.date_time_utils.convert_string_to_local_date_time \
            import convert_string_to_local_date_time
        from ib_common.date_time_utils.convert_datetime_to_local_string \
            import convert_datetime_to_local_string
        date_time_format = '%Y-%m-%d %H:%M:%S'

        date_range = {
            "from_date": convert_string_to_local_date_time(from_date,
                                                           date_time_format),
            "to_date": convert_string_to_local_date_time(to_date,
                                                         date_time_format)
        }

        transactions = Statement.get_transactions(
            customer_id=self.customer_id, date_range=date_range)

        for each in transactions:
            each["date_time"] = convert_datetime_to_local_string(
                each["date_time"], date_time_format)

        customer_transactions = [each for each in self.transactions if
                                 each["customer_id"] == self.customer_id]
        self.assertItemsEqual(customer_transactions, transactions)

    def test_case_no_transactions_for_customer(self):
        self.setup_statements_for_both_customers()

        from wallet.models import Statement

        from_date = "2017-12-12 13:00:00"
        to_date = "2017-12-16 13:00:00"
        date_range = {
            "from_date": from_date,
            "to_date": to_date
        }

        from ib_common.date_time_utils.convert_datetime_to_local_string \
            import convert_datetime_to_local_string
        date_time_format = '%Y-%m-%d %H:%M:%S'

        parsed_date_range = self._get_parsed_date_range(date_range=date_range)
        transactions = Statement.get_transactions(
            customer_id=self.no_transactions_customer_id,
            date_range=parsed_date_range
        )

        for each in transactions:
            each["date_time"] = convert_datetime_to_local_string(
                each["date_time"], date_time_format)

        customer_transactions = self._get_customer_transactions(
            date_range=date_range,
            customer_id=self.no_transactions_customer_id
        )

        self.assertItemsEqual(customer_transactions, transactions)

    def test_case_invalid_date_range(self):
        self.setup_statements_for_both_customers()

        from wallet.models import Statement

        from_date = "2017-12-16 13:00:00"
        to_date = "2017-12-12 13:00:00"

        from ib_common.date_time_utils.convert_string_to_local_date_time \
            import convert_string_to_local_date_time
        date_time_format = '%Y-%m-%d %H:%M:%S'

        date_range = {
            "from_date": convert_string_to_local_date_time(from_date,
                                                           date_time_format),
            "to_date": convert_string_to_local_date_time(to_date,
                                                         date_time_format)
        }

        from wallet.exceptions.exceptions import InvalidDateRangeException
        from wallet.constants.exception_constants import INVALID_DATE_RANGE
        with self.assertRaisesMessage(InvalidDateRangeException,
                                      INVALID_DATE_RANGE):
            Statement.get_transactions(
                customer_id=self.customer_id,
                date_range=date_range
            )
