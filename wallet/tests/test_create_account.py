from django.test import TestCase


class TestCreateAccount(TestCase):

    def testcase_create_account(self):
        customer_id = 'customer1'
        from wallet.models import Account
        Account.create_account(customer_id)

        account_objects = Account.objects.all()
        account_object = account_objects[0]

        self.assertEqual(account_objects.count(), 1)
        self.assertEqual(account_object.customer_id, customer_id)

    def testcase_create_multiple_accounts_for_different_users(self):
        customer_id_1 = 'customer1'
        customer_id_2 = 'customer2'

        from wallet.models import Account

        Account.create_account(customer_id_1)
        Account.create_account(customer_id_2)

        account_objects = Account.objects.all()
        customer_ids = [each.customer_id for each in account_objects]

        self.assertEqual(account_objects.count(), 2)
        self.assertItemsEqual(customer_ids, [customer_id_1, customer_id_2])

    def testcase_multiple_accounts_for_same_user(self):
        customer_id = 'customer1'

        from wallet.models import Account
        Account.create_account(customer_id)

        from wallet.exceptions.exceptions import MultipleAccountsException
        from wallet.constants.exception_constants import MULTIPLE_ACCOUNTS
        with self.assertRaisesMessage(MultipleAccountsException,
                                      MULTIPLE_ACCOUNTS):
            Account.create_account(customer_id)

    def testcase_joint_account_holder(self):
        customer_id_1 = 'customer1'
        customer_id_2 = 'customer2'

        from wallet.models import Account

        account_id = '200802022'

        Account._assign_account_id_to_customer(account_id=account_id,
                                               customer_id=customer_id_1)
        self.assertRaises(Exception,
                          lambda: Account._assign_account_id_to_customer(
                              account_id=account_id,
                              customer_id=customer_id_2))
