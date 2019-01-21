from django.test import TestCase


class TestTransferMoney(TestCase):
    customer_id_1 = 'customer1'
    customer_id_2 = 'customer2'

    initial_balance_of_customer_id_1 = 10
    initial_balance_of_customer_id_2 = 10

    def setUp(self):
        from wallet.models import Account
        Account.create_account(self.customer_id_1)
        Account.add_balance(self.customer_id_1,
                            self.initial_balance_of_customer_id_1)
        Account.create_account(self.customer_id_2)
        Account.add_balance(self.customer_id_2,
                            self.initial_balance_of_customer_id_2)

    def testcase_transfer_money(self):
        from wallet.models import Account
        prev_balance_of_customer_1 = Account.get_balance(
            customer_id=self.customer_id_1)
        prev_balance_of_customer_2 = Account.get_balance(
            customer_id=self.customer_id_2)

        amount_to_transfer = 5

        Account.transfer_money(
            from_customer_id=self.customer_id_1,
            to_customer_id=self.customer_id_2,
            money=amount_to_transfer
        )

        current_balance_of_customer_1 = Account.get_balance(
            customer_id=self.customer_id_1)
        current_balance_of_customer_2 = Account.get_balance(
            customer_id=self.customer_id_2)

        amount_debited_for_customer_1 = prev_balance_of_customer_1 - current_balance_of_customer_1
        amount_credited_for_customer_2 = current_balance_of_customer_2 - prev_balance_of_customer_2

        self.assertEquals(amount_debited_for_customer_1, amount_to_transfer)
        self.assertEquals(amount_credited_for_customer_2, amount_to_transfer)

    def testcase_transfer_in_sufficient_money(self):
        from wallet.models import Account
        prev_balance_of_customer_1 = Account.get_balance(
            customer_id=self.customer_id_1)
        prev_balance_of_customer_2 = Account.get_balance(
            customer_id=self.customer_id_2)

        amount_to_transfer = 20

        self.assertRaises(Exception, lambda: Account.transfer_money(
            from_customer_id=self.customer_id_1,
            to_customer_id=self.customer_id_2,
            money=amount_to_transfer
        ))

        current_balance_of_customer_1 = Account.get_balance(
            customer_id=self.customer_id_1)
        current_balance_of_customer_2 = Account.get_balance(
            customer_id=self.customer_id_2)

        amount_debited_for_customer_1 = prev_balance_of_customer_1 - current_balance_of_customer_1
        amount_credited_for_customer_2 = current_balance_of_customer_2 - prev_balance_of_customer_2

        self.assertEquals(amount_debited_for_customer_1, 0)
        self.assertEquals(amount_credited_for_customer_2, 0)

    def testcase_transfer_non_negative_money(self):
        from wallet.models import Account
        prev_balance_of_customer_1 = Account.get_balance(
            customer_id=self.customer_id_1)
        prev_balance_of_customer_2 = Account.get_balance(
            customer_id=self.customer_id_2)

        amount_to_transfer = -1

        self.assertRaises(Exception, lambda: Account.transfer_money(
            from_customer_id=self.customer_id_1,
            to_customer_id=self.customer_id_2,
            money=amount_to_transfer
        ))

        current_balance_of_customer_1 = Account.get_balance(
            customer_id=self.customer_id_1)
        current_balance_of_customer_2 = Account.get_balance(
            customer_id=self.customer_id_2)

        amount_debited_for_customer_1 = prev_balance_of_customer_1 - current_balance_of_customer_1
        amount_credited_for_customer_2 = current_balance_of_customer_2 - prev_balance_of_customer_2

        self.assertEquals(amount_debited_for_customer_1, 0)
        self.assertEquals(amount_credited_for_customer_2, 0)
