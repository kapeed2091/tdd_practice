from django.test import TestCase


class TestGetStatement(TestCase):
    customer_id_1 = 'customer1'
    customer_id_2 = 'customer2'

    def setUp(self):
        from wallet.models import Account

        Account.create_account(self.customer_id_1)
        Account.create_account(self.customer_id_2)

        account = Account.get_account(self.customer_id_1)
        Account.add_balance(account=account, amount=100)
        Account.transfer_amount(sender_id=self.customer_id_1, receiver_id=self.customer_id_2, amount=50)
