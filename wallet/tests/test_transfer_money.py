from django.test import TestCase


class TestTransferMoney(TestCase):
    customer_id = 'customer1'
    beneficiary_customer_id = 'customer2'

    def testcase_insufficient_balance_to_transfer(self):
        from wallet.models import Account
        Account.create_account(self.customer_id)
        Account.create_account(self.beneficiary_customer_id)
        Account.add_balance(customer_id=self.customer_id, amount=1000)

        with self.assertRaises(Exception):
            Account.transfer_money(self.customer_id,
                                   self.beneficiary_customer_id,
                                   10000)

    def testcase_transfer_amount_gt_zero(self):
        from wallet.models import Account
        Account.create_account(self.customer_id)
        Account.create_account(self.beneficiary_customer_id)
        Account.add_balance(customer_id=self.customer_id, amount=1000)

        with self.assertRaises(Exception):
            Account.transfer_money(self.customer_id,
                                   self.beneficiary_customer_id,
                                   -3)
