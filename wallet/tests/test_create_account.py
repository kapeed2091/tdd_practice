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
        
        account_details_1 = Account.create_account(customer_id_1)
        account_details_2 = Account.create_account(customer_id_2)
        
        self.assertEquals(account_details_1['customer_id'], customer_id_1, 'Issue with customer_id')
        self.assertEquals(account_details_2['customer_id'], customer_id_2, 'Issue with customer_id')
        self.assertNotEqual(account_details_1['account_id'], account_details_2['account_id'])

    def testcase_multiple_accounts_for_same_user(self):
        customer_id = 'customer1'

        from wallet.models import Account

        Account.create_account(customer_id)
        self.assertRaises(Exception, lambda: Account.create_account(customer_id))

    def testcase_joint_account_holder(self):
        customer_id_1 = 'customer1'
        customer_id_2 = 'customer2'

        from wallet.models import Account

        account_id = '200802022'

        Account._assign_account_id_to_customer(account_id=account_id,
                                               customer_id=customer_id_1)
        self.assertRaises(Exception, lambda: Account._assign_account_id_to_customer(account_id=account_id,
                                                                                    customer_id=customer_id_2))