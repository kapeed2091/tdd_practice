from django.test import TestCase


class TestTransferAmount(TestCase):
    customer_id1 = 'customer1'
    customer_id2 = 'customer2'
    account_id1 = None
    account_id2 = None

    def setUp(self):
        from wallet.models import Account

        account_details1 = Account.create_account(self.customer_id1)
        self.account_id1 = account_details1['account_id']

        account_details2 = Account.create_account(self.customer_id2)
        self.account_id2 = account_details2['account_id']

    def testcase_transfer_amount(self):
        from wallet.models import Account
        transfer_amount = 10

        Account.add_balance(customer_id=self.customer_id1, amount=100)

        prev_customer_id1_balance = Account.get_balance(self.customer_id1)
        prev_customer_id2_balance = Account.get_balance(self.customer_id2)

        Account.transfer_amount(source_customer_id=self.customer_id1,
                                destination_customer_id=self.customer_id2,
                                transfer_amount=transfer_amount)

        customer_id1_balance = Account.get_balance(self.customer_id1)
        customer_id2_balance = Account.get_balance(self.customer_id2)

        self.assertEquals(customer_id1_balance,
                          prev_customer_id1_balance-transfer_amount)
        self.assertEquals(customer_id2_balance,
                          prev_customer_id2_balance + transfer_amount)

    def test_case_transfer_negative_amount(self):
        from wallet.models import Account

        transfer_amount = -10

        with self.assertRaisesMessage(
                Exception,
                expected_message='Can not transfer the given amount'):
            Account.transfer_amount(source_customer_id=self.customer_id1,
                                    destination_customer_id=self.customer_id2,
                                    transfer_amount=transfer_amount)

    def test_case_transfer_zero_balance(self):
        from wallet.models import Account

        transfer_amount = 0

        with self.assertRaisesMessage(
                Exception,
                expected_message='Can not transfer the given amount'):
            Account.transfer_amount(source_customer_id=self.customer_id1,
                                    destination_customer_id=self.customer_id2,
                                    transfer_amount=transfer_amount)

    def test_case_transfer_float_balance(self):
        from wallet.models import Account

        transfer_amount = 0

        with self.assertRaisesMessage(
                Exception,
                expected_message='Can not transfer the given amount'):
            Account.transfer_amount(source_customer_id=self.customer_id1,
                                    destination_customer_id=self.customer_id2,
                                    transfer_amount=transfer_amount)
