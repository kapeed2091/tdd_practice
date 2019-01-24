from django.test import TestCase

customer_1_transactions = [
    {
        'amount': 100,
        'transaction_type': 'CREDIT'
    },
    {
        'amount': 10,
        'transaction_type': 'DEBIT'
    }
]

customer_2_transactions = [
    {
        'amount': 10,
        'transaction_type': 'CREDIT'
    },
    {
        'amount': 10,
        'transaction_type': 'DEBIT'
    }
]

customer_1_transactions_with_dates = [
    {
        'amount': 100,
        'transaction_type': 'CREDIT',
        'date': '2019-01-23 10:00:00'
    },
    {
        'amount': 10,
        'transaction_type': 'DEBIT',
        'date': '2019-01-23 11:10:00'
    }
]

customer_2_transactions_with_dates = [
    {
        'amount': 10,
        'transaction_type': 'CREDIT',
        'date': '2019-01-23 10:30:00'
    },
    {
        'amount': 10,
        'transaction_type': 'DEBIT',
        'date': '2019-01-23 11:20:00'
    }
]


class TestGetStatement(TestCase):
    customer_id_1 = 'customer1'
    customer_id_2 = 'customer2'

    @staticmethod
    def create_transactions(customer_id, transactions_list):
        from wallet_v2.models import Transaction, Account
        from ib_common.date_time_utils.convert_string_to_local_date_time \
            import convert_string_to_local_date_time
        from wallet_v2.constants.general import DEFAULT_DATE_TIME_FORMAT

        account = Account.get_account(customer_id=customer_id)
        for transaction in transactions_list:
            transaction_date = convert_string_to_local_date_time(
                transaction['date'], DEFAULT_DATE_TIME_FORMAT)
            Transaction.objects.create(
                account_id=account.id,
                amount=transaction['amount'],
                transaction_type=transaction['transaction_type'],
                transaction_date=transaction_date)

    def testcase_get_customer_statement(self):
        from wallet_v2.models import Account, Transaction

        Account.create_account(self.customer_id_1)
        Account.create_account(self.customer_id_2)
        self.create_transactions(
            self.customer_id_1, customer_1_transactions_with_dates)
        self.create_transactions(
            self.customer_id_2, customer_2_transactions_with_dates)

        customer_transactions = Transaction.get_statement(
            self.customer_id_1)
        self.assertItemsEqual(customer_transactions, customer_1_transactions)

    def testcase_get_customer_statement_in_date_range(self):
        from wallet_v2.models import Account, Transaction

        Account.create_account(self.customer_id_1)
        Account.create_account(self.customer_id_2)
        self.create_transactions(
            self.customer_id_1, customer_1_transactions_with_dates)
        self.create_transactions(
            self.customer_id_2, customer_2_transactions_with_dates)

        customer_transactions = \
            Transaction.get_statement_within_date_range(
                self.customer_id_1, from_date_str='2019-01-23 10:00:00',
                to_date_str='2019-01-23 11:00:00')

        expected_transactions = [
            {
                'amount': 100,
                'transaction_type': 'CREDIT',
                'date': '2019-01-23 10:00:00'
            }
        ]
        self.assertItemsEqual(customer_transactions, expected_transactions)

    def testcase_customer_should_have_account_to_get_statement(self):
        from wallet_v2.models import Transaction
        with self.assertRaisesMessage(Exception, "Customer does not exist"):
            Transaction.get_statement(self.customer_id_1)

    def testcase_customer_should_have_account_to_get_statement_in_date_range(
            self):
        from wallet_v2.models import Transaction
        with self.assertRaisesMessage(Exception, "Customer does not exist"):
            Transaction.get_statement_within_date_range(
                self.customer_id_1, from_date_str='2019-01-23 10:00:00',
                to_date_str='2019-01-23 11:00:00')
