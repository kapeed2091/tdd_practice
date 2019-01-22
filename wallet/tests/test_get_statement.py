from django.test import TestCase
import datetime


class TestGetStatement(TestCase):
    customer_id = 'customer1'
    transactions = [
        {
            "date_time": datetime.datetime(2017, 12, 12, 13, 0, 0),
            "amount": 100,
            "status": "DEBIT"
        },
        {
            "date_time": datetime.datetime(2017, 12, 13, 13, 0, 0),
            "amount": 110,
            "status": "CREDIT"
        },
        {
            "date_time": datetime.datetime(2017, 12, 14, 13, 0, 0),
            "amount": 120,
            "status": "DEBIT"
        },
        {
            "date_time": datetime.datetime(2017, 12, 15, 13, 0, 0),
            "amount": 130,
            "status": "CREDIT"
        }
    ]

    def setUp(self):
        from wallet.models import Statement
        Statement.add_transactions(self.transactions)

    def test_get_balance_successful(self):
        from wallet.models import Statement

        from_date = datetime.datetime(2017, 12, 12, 12, 0, 0)
        to_date = datetime.datetime(2017, 12, 16, 12, 0, 0)

        date_range = {
            "from_date": from_date,
            "to_date": to_date
        }

        transactions = Statement.get_transactions(date_range=date_range)

        self.assertItemsEqual(self.transactions, transactions)
