from django.test import TestCase


class TestAddBalance(TestCase):
    customer_id = 'customer1'
    account_id = None

    def setUp(self):
        from wallet.models import Account
        account_details = Account.create_account(self.customer_id)
        self.account_id = account_details['account_id']

    def testcase_add_balance(self):
        from wallet.models import Account
        account = Account.get_account(self.customer_id)
        prev_balance = account.balance
        Account.add_balance(account=account, amount=10)
        balance = Account.get_balance(self.customer_id)

        self.assertEquals(balance, prev_balance+10)

    def testcase_add_negative_balance(self):
        from wallet.models import Account
        with self.assertRaises(Exception):
            account = Account.get_account(self.customer_id)
            Account.add_balance(account=account, amount=-10)

    # def testcase_add_balance_and_check_transaction_entry(self):
    #     from wallet.models import Account, Transaction
    #     account = Account.get_account(self.customer_id)
    #     Account.add_balance(account=account, amount=10)
    #     transactions = Transaction.get_transactions(self.customer_id)
    #     self.assertEqual(len(transactions), 1)
    #
    #     transaction = transactions[0]
    #     self.assertEqual(transaction.amount, 10)
