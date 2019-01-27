"""Adapter for Django ORM.

Pretty much all calls to the database in the live app should go through the methods of this class.
The MemoryStorage class shares the same interface, but doesn't depend on an actual database. It can
be swapped out for this one when testing use cases.
"""

from .storage import Storage
from wallet import models as wallet_models


class DjangoStorage(Storage):
    """Adapter to use Django ORM as a storage backend."""

    def create_account(self, customer_id, account_id):
        account = wallet_models.Account.objects.create(
            customer_id=customer_id, account_id=account_id)
        return account.to_entity()

    def add_balance(self, customer_id, balance):
        account = wallet_models.Account.objects.get(customer_id=customer_id)
        account.balance += balance
        account.save()

    def __get_account(self, customer_id):
        return wallet_models.Account.objects.get(customer_id=customer_id)

    def transfer_balance(self, sender_id, receiver_id, balance):
        sender_account = self.__get_account(customer_id=sender_id)
        receiver_account = self.__get_account(customer_id=receiver_id)

        sender_account.balance -= balance
        sender_account.save()

        receiver_account.balance -= balance
        receiver_account.save()

    def get_transactions(self, customer_id):
        transactions = wallet_models.Transaction.objects.filter(
            customer_id=customer_id)
        return [transaction.to_entity() for transaction in transactions]
