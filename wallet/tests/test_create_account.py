from django.test import TestCase


class TestCreateAccount(TestCase):
    
    def testcase_create_account(self):
        from wallet.models import Account

        customer_id = 'customer1'
        Account.create_account_if_does_not_exist(customer_id)
        account_details = Account.get_account(customer_id)

        self.assertEquals(account_details.customer_id, customer_id, 'Issue with customer_id')
        self.assertNotEqual(account_details.account_id, None, 'Issue with account_id')

    def testcase_create_multiple_accounts_for_different_users(self):
        from wallet.models import Account

        customer_id_1 = 'customer1'
        customer_id_2 = 'customer2'
        Account.create_account_if_does_not_exist(customer_id_1)
        Account.create_account_if_does_not_exist(customer_id_2)
        account_details_1 = Account.get_account(customer_id_1)
        account_details_2 = Account.get_account(customer_id_2)
        
        self.assertEquals(account_details_1.customer_id, customer_id_1, 'Issue with customer_id')
        self.assertEquals(account_details_2.customer_id, customer_id_2, 'Issue with customer_id')
        self.assertNotEqual(account_details_1.account_id, account_details_2.account_id)

    def testcase_multiple_accounts_for_same_user(self):
        from wallet.models import Account

        customer_id = 'customer1'
        Account.create_account_if_does_not_exist(customer_id)
        self.assertRaises(Exception, lambda: Account.create_account_if_does_not_exist(customer_id))

    def testcase_joint_account_holder(self):
        from wallet.models import Account

        customer_id_1 = 'customer1'
        customer_id_2 = 'customer2'
        account_id = '200802022'
        Account._create_account(account_id=account_id,
                                customer_id=customer_id_1)
        self.assertRaises(Exception, lambda: Account._create_account(account_id=account_id,
                                                                     customer_id=customer_id_2))