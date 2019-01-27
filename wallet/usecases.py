class AccountUseCases():
    def __init__(self, storage):
        self.storage = storage

    def create_account(self, customer_id):
        import uuid
        account_id = str(uuid.uuid4())[0:20]
        return self.storage.create_account(customer_id, account_id)

    def add_balance(self, customer_id, amount):
        return self.storage.add_balance(customer_id=customer_id,
                                        balance=amount)

    def transfer_balance(self, sender_id, receiver_id, amount):
        return self.storage.transfer_balance(
            sender_id=sender_id, receiver_id=receiver_id, balance=amount)

    def get_transactions(self, customer_id):
        return self.storage.get_transactions(customer_id=customer_id)
