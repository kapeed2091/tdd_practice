from django.test import TestCase

class TestCreateAccount(TestCase):
    
    def testcase1(self):
        customer_id = 'customer1'
        from wallet.models import Account
        account_details = Account.create_account(customer_id)
        self.assertEquals(account_details['customer_id'], customer_id, 'Issue with customer_id')
        self.assertNotEqual(account_details['account_id'], None, 'Issue with account_id')

    def testcase2(self):
        customer_id_1 = 'customer1'
        customer_id_2 = 'customer2'
        
        from wallet.models import Account
        
        account_details_1 = Account.create_account(customer_id_1)
        account_details_2 = Account.create_account(customer_id_2)
        
        self.assertEquals(account_details_1['customer_id'], customer_id_1, 'Issue with customer_id')
        self.assertEquals(account_details_2['customer_id'], customer_id_2, 'Issue with customer_id')
        self.assertNotEqual(account_details_1['account_id'], account_details_2['account_id'])
