from django.test import TestCase
from wallet.models import Account


class TestTransferAmount(TestCase):
    customer_id_1 = 'customer1'
    customer_id_2 = 'customer2'

    def setUp(self):
        Account.create_account(customer_id=self.customer_id_1)
        Account.add_balance(customer_id=self.customer_id_1, amount=100)

        Account.create_account(customer_id=self.customer_id_2)
        Account.add_balance(customer_id=self.customer_id_2, amount=100)

    def test_case_successful_transfer(self):
        prev_balance_of_customer_1 = Account.get_balance(
            customer_id=self.customer_id_1)
        prev_balance_of_customer_2 = Account.get_balance(
            customer_id=self.customer_id_2)
        Account.transfer_amount(
            amount=10, transferee_customer_id=self.customer_id_1,
            transferred_customer_id=self.customer_id_2)
        post_balance_of_customer_1 = Account.get_balance(
            customer_id=self.customer_id_1)
        post_balance_of_customer_2 = Account.get_balance(
            customer_id=self.customer_id_2)

        amount_deducted_for_customer_1 = \
            prev_balance_of_customer_1 - post_balance_of_customer_1
        amount_added_for_customer_2 = \
            post_balance_of_customer_2 - prev_balance_of_customer_2

        self.assertEqual(amount_deducted_for_customer_1, 10)
        self.assertEqual(amount_added_for_customer_2, 10)
