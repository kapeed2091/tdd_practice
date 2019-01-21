from django.test import TestCase


class TestTransferMoney(TestCase):
    customer_id_1 = 'customer1'
    customer_id_2 = 'customer2'

    initial_balance_of_customer_id_1 = 10
    initial_balance_of_customer_id_2 = 10

    def setUp(self):
        from wallet.models import Account
        Account.create_account(self.customer_id_1)
        Account.create_account(self.customer_id_2)

    def testcase_get_statement(self):
        from wallet.models import Account
        Account.add_balance(self.customer_id_1,
                            self.initial_balance_of_customer_id_1)
        Account.add_balance(self.customer_id_2,
                            self.initial_balance_of_customer_id_2)

        amount_to_transfer = 5
        Account.transfer_money(
            from_customer_id=self.customer_id_1,
            to_customer_id=self.customer_id_2,
            money=amount_to_transfer
        )

        from wallet.models import Transaction
        customer_1_statements = Transaction.get_statement(
            customer_id=self.customer_id_1)

        add_balance_statement_for_customer_1 = customer_1_statements[0]
        self.assertEqual(
            add_balance_statement_for_customer_1['transaction_type'],
            TransactionType.ADD_BALANCE.value)
        self.assertEqual(
            add_balance_statement_for_customer_1['transaction_money'],
            self.initial_balance_of_customer_id_1)

        credit_money_statement_for_customer_1 = customer_1_statements[1]
        self.assertEqual(
            credit_money_statement_for_customer_1['transaction_type'],
            TransactionType.MONEY_CREDITED.value)
        self.assertEqual(
            credit_money_statement_for_customer_1['transaction_money'],
            amount_to_transfer)

        customer_2_statements = Transaction.get_statement(
            customer_id=self.customer_id_2)

        add_balance_statement_for_customer_2 = customer_2_statements[0]
        self.assertEqual(
            add_balance_statement_for_customer_2['transaction_type'],
            TransactionType.ADD_BALANCE.value)
        self.assertEqual(
            add_balance_statement_for_customer_2['transaction_money'],
            self.initial_balance_of_customer_id_2)

        debit_money_statement_for_customer_2 = customer_2_statements[1]
        self.assertEqual(
            debit_money_statement_for_customer_2['transaction_type'],
            TransactionType.MONEY_DEBITED.value)
        self.assertEqual(
            debit_money_statement_for_customer_2['transaction_money'],
            amount_to_transfer)
