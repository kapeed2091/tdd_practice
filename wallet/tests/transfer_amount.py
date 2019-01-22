from django.test import TestCase
from wallet.models import Account


class TestTransferAmount(TestCase):
    customer_id_1 = 'customer1'
    customer_id_2 = 'customer2'

    def setup_both_customers(self):
        self.setup_customer_1()
        self.setup_customer_2()

    def setup_customer_1(self):
        Account.create_account(customer_id=self.customer_id_1)
        Account.add_balance(customer_id=self.customer_id_1, amount=100)

    def setup_customer_2(self):
        Account.create_account(customer_id=self.customer_id_2)
        Account.add_balance(customer_id=self.customer_id_2, amount=100)

    def test_case_successful_transfer(self):
        self.setup_both_customers()

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

    def test_case_insufficient_funds(self):
        self.setup_both_customers()

        from wallet.exceptions.exceptions import InsufficientFund
        from wallet.constants.exception_constants import \
            INSUFFICIENT_FUND
        with self.assertRaisesMessage(InsufficientFund, INSUFFICIENT_FUND):
            Account.transfer_amount(
                amount=1000, transferee_customer_id=self.customer_id_1,
                transferred_customer_id=self.customer_id_2)

    def test_case_negative_amount(self):
        self.setup_both_customers()

        from wallet.exceptions.exceptions import \
            NegativeAmountTransferException
        from wallet.constants.exception_constants import \
            NEGATIVE_AMOUNT_TRANSFER
        with self.assertRaisesMessage(NegativeAmountTransferException,
                                      NEGATIVE_AMOUNT_TRANSFER):
            Account.transfer_amount(
                amount=-100, transferee_customer_id=self.customer_id_1,
                transferred_customer_id=self.customer_id_2)

    def test_case_invalid_sender_customer_id(self):
        self.setup_customer_2()

        from wallet.exceptions.exceptions import \
            InvalidSenderCustomerIdException
        from wallet.constants.exception_constants import \
            CUSTOMER_DOES_NOT_EXIST
        with self.assertRaisesMessage(InvalidSenderCustomerIdException,
                                      CUSTOMER_DOES_NOT_EXIST):
            Account.transfer_amount(
                amount=100, transferee_customer_id=self.customer_id_1,
                transferred_customer_id=self.customer_id_2)

    def test_case_no_transferred_account(self):
        self.setup_customer_1()

        with self.assertRaises(Account.DoesNotExist):
            Account.transfer_amount(
                amount=100, transferee_customer_id=self.customer_id_1,
                transferred_customer_id=self.customer_id_2)

    def test_case_invalid_amount(self):
        self.setup_both_customers()

        from wallet.exceptions.exceptions import InvalidAmountType
        from wallet.constants.exception_constants import \
            INVALID_AMOUNT_TYPE
        with self.assertRaisesMessage(InvalidAmountType, INVALID_AMOUNT_TYPE):
            Account.transfer_amount(
                amount=100.13, transferee_customer_id=self.customer_id_1,
                transferred_customer_id=self.customer_id_2)