from django.test import TestCase


class TestTransferMoney(TestCase):
    payee_customer_id = 'customer1'
    beneficiary_customer_id = 'customer2'

    def testcase_transfer_money(self):
        from wallet.models import Account
        Account.create_account(self.payee_customer_id)
        Account.create_account(self.beneficiary_customer_id)
        Account.add_balance(self.payee_customer_id, 1000)

        pre_transfer_payee_balance = Account.get_balance(self.payee_customer_id)
        pre_transfer_beneficiary_balance = Account.get_balance(
            self.beneficiary_customer_id)

        Account.transfer_money(self.payee_customer_id,
                               self.beneficiary_customer_id,
                               100)

        post_transfer_payee_balance = Account.get_balance(self.payee_customer_id)
        post_transfer_beneficiary_balance = Account.get_balance(
            self.beneficiary_customer_id)

        self.assertEqual(
            pre_transfer_payee_balance - post_transfer_payee_balance, 100,
            "Incorrect balance for payee")
        self.assertEqual(
            post_transfer_beneficiary_balance - pre_transfer_beneficiary_balance,
            100, "Incorrect balance for beneficiary")
