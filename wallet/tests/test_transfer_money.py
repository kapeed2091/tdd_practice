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

    def testcase_payee_should_have_account(self):
        from wallet.models import Account
        Account.create_account(self.beneficiary_customer_id)

        with self.assertRaises(Exception):
            Account.transfer_money(self.customer_id,
                                   self.beneficiary_customer_id,
                                   10000)

    def testcase_beneficiary_should_have_account(self):
        from wallet.models import Account
        Account.create_account(self.customer_id)
        Account.add_balance(self.customer_id, 1000)

        with self.assertRaises(Exception):
            Account.transfer_money(self.customer_id,
                                   self.beneficiary_customer_id,
                                   100)

    def testcase_transfer_money(self):
        from wallet.models import Account
        Account.create_account(self.customer_id)
        Account.create_account(self.beneficiary_customer_id)
        Account.add_balance(self.customer_id, 1000)

        pre_transfer_payee_balance = Account.get_balance(self.customer_id)
        pre_transfer_beneficiary_balance = Account.get_balance(
            self.beneficiary_customer_id)

        Account.transfer_money(self.customer_id,
                               self.beneficiary_customer_id,
                               100)

        post_transfer_payee_balance = Account.get_balance(self.customer_id)
        post_transfer_beneficiary_balance = Account.get_balance(
            self.beneficiary_customer_id)

        self.assertEquals(
            pre_transfer_payee_balance - post_transfer_payee_balance, 100,
            'Incorrect balance for payee')
        self.assertEquals(
            post_transfer_beneficiary_balance - pre_transfer_beneficiary_balance,
            100, 'Incorrect balance for beneficiary')
