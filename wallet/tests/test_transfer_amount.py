from django.test import TestCase


class TestTransferAmount(TestCase):
    customer_id1 = 'customer1'
    customer_id2 = 'customer2'

    def setUp(self):
        from wallet.models import Account

        Account.create_account(self.customer_id1)
        Account.create_account(self.customer_id2)

    def testcase_transfer_amount(self):
        from wallet.models import Account
        transfer_amount = 10

        prev_customer_id1_balance = Account.get_balance(self.customer_id1)
        prev_customer_id2_balance = Account.get_balance(self.customer_id2)

        Account.add_balance(customer_id=self.customer_id1, amount=100)

        Account.transfer_amount(from_customer_id=self.customer_id1,
                                to_customer_id=self.customer_id2,
                                transfer_amount=transfer_amount)

        customer_id1_balance = Account.get_balance(self.customer_id1)
        customer_id2_balance = Account.get_balance(self.customer_id2)

        self.assertEquals(customer_id1_balance,
                          prev_customer_id1_balance-transfer_amount)
        self.assertEquals(customer_id2_balance,
                          prev_customer_id2_balance + transfer_amount)
