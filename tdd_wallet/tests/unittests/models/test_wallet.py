from django.test import TestCase


class TestWallet(TestCase):
    def test_case(self):
        from tdd_wallet.models import Wallet
        customer_id = 'string'
        balance = 10
        Wallet.objects.create(customer_id=customer_id, balance=balance)
        wallet = Wallet.objects.first()
        self.assertEqual(wallet.customer_id, customer_id)
        self.assertEqual(wallet.balance, balance)