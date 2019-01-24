from django.test import TestCase


class TestTransferBalance(TestCase):
    payer_customer_id = 'customer1'
    beneficiary_customer_id = 'customer2'

    def testcase_transfer_money(self):
        from wallet_v2.models import Account

        Account.create_account(self.payer_customer_id)
        Account.add_balance(self.payer_customer_id, 1000)
        Account.create_account(self.beneficiary_customer_id)

        pre_transfer_payer_balance = Account.get_balance(self.payer_customer_id)
        pre_transfer_beneficiary_balance = Account.get_balance(
            self.beneficiary_customer_id)
        Account.transfer_balance(self.payer_customer_id,
                                 self.beneficiary_customer_id, 100)
        post_transfer_payer_balance = Account.get_balance(
            self.payer_customer_id)
        post_transfer_beneficiary_balance = Account.get_balance(
            self.beneficiary_customer_id)

        self.assertEqual(
            pre_transfer_payer_balance - post_transfer_payer_balance, 100)
        self.assertEqual(
            post_transfer_beneficiary_balance -
            pre_transfer_beneficiary_balance, 100)

    def testcase_transfer_negative_balance(self):
        from wallet_v2.models import Account

        Account.create_account(self.payer_customer_id)
        Account.create_account(self.beneficiary_customer_id)

        with self.assertRaisesMessage(
                Exception, "Transfer amount should be greater than zero"):
            Account.transfer_balance(self.payer_customer_id,
                                     self.beneficiary_customer_id, -2)

    def testcase_payer_should_have_sufficient_balance(self):
        from wallet_v2.models import Account

        Account.create_account(self.payer_customer_id)
        Account.create_account(self.beneficiary_customer_id)

        with self.assertRaisesMessage(
                Exception, "Insufficient balance to transfer money"):
            Account.transfer_balance(self.payer_customer_id,
                                     self.beneficiary_customer_id, 100)

    def testcase_payer_and_beneficiary_should_not_be_same(self):
        from wallet_v2.models import Account

        Account.create_account(self.payer_customer_id)

        with self.assertRaisesMessage(
                Exception, "Payer and Beneficiary should not be same"):
            Account.transfer_balance(self.payer_customer_id,
                                     self.payer_customer_id, 100)

    def testcase_create_transactions_for_credit_and_debit_amount(self):
        from wallet_v2.models import Account, Transaction

        Account.create_account(self.payer_customer_id)
        Account.create_account(self.beneficiary_customer_id)
        Account.add_balance(self.payer_customer_id, 1000)

        Account.transfer_balance(
            self.payer_customer_id, self.beneficiary_customer_id, 100)

        payer_transactions_count = Transaction.objects.filter(
            account__customer_id=self.payer_customer_id).count()
        beneficiary_transactions_count = Transaction.objects.filter(
            account__customer_id=self.beneficiary_customer_id).count()

        self.assertEqual(payer_transactions_count, 2)
        self.assertEqual(beneficiary_transactions_count, 1)
