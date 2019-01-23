from django.db import models


class Account(models.Model):
    CUSTOMER_ID_LENGTH = 20
    ACCOUNT_ID_LENGTH = 20
    DEFAULT_BALANCE = 0
    MINIMUM_TRANSACTION_AMOUNT_SHOULD_BE_GREATER_THAN = 0

    customer_id = models.CharField(max_length=CUSTOMER_ID_LENGTH, unique=True)
    account_id = models.CharField(max_length=ACCOUNT_ID_LENGTH, unique=True)
    balance = models.IntegerField(default=DEFAULT_BALANCE)

    @classmethod
    def create_account_if_does_not_exist(cls, customer_id):
        if cls._is_customer_account_exists(customer_id):
            raise Exception

        account_id = cls.generate_account_id(cls.ACCOUNT_ID_LENGTH)
        cls._create_account(
            account_id=account_id, customer_id=customer_id)

    @classmethod
    def _is_customer_account_exists(cls, customer_id):
        return cls.objects.filter(customer_id=customer_id).exists()

    @classmethod
    def _create_account(cls, account_id, customer_id):
        return cls.objects.create(
            account_id=account_id, customer_id=customer_id)

    @staticmethod
    def generate_account_id(length):
        import uuid
        return str(uuid.uuid4())[0:length]

    @classmethod
    def get_balance(cls, customer_id):
        account = cls.objects.get(customer_id=customer_id)
        return account.balance

    def add_balance_if_amount_is_valid(self, amount):
        from wallet.models import Transaction

        if self.is_invalid_amount(amount):
            raise Exception('Invalid amount')

        self.balance += amount
        self.save()
        Transaction.create_transaction(account=self, amount=amount)

    def _remove_balance_if_amount_is_valid(self, amount):
        from wallet.models import Transaction

        if self.is_invalid_amount(amount):
            raise Exception('Invalid amount')

        balance = self.balance
        if amount > balance:
            raise Exception('Insufficient balance')

        self.balance = balance - amount
        self.save()
        Transaction.create_transaction(account=self, amount=-amount)

    @classmethod
    def is_invalid_amount(cls, amount):
        if amount <= cls.MINIMUM_TRANSACTION_AMOUNT_SHOULD_BE_GREATER_THAN:
            return True
        return False

    @classmethod
    def get_account(cls, customer_id):
        return cls.objects.get(customer_id=customer_id)

    @classmethod
    def transfer_amount_if_accounts_and_amount_is_valid(cls, sender_id, receiver_id, amount):
        try:
            sender_account = cls.get_account(sender_id)
        except cls.DoesNotExist:
            raise Exception('Invalid sender id')

        try:
            receiver_account = cls.get_account(receiver_id)
        except cls.DoesNotExist:
            raise Exception('Invalid receiver id')

        sender_account._remove_balance_if_amount_is_valid(amount=amount)
        receiver_account.add_balance_if_amount_is_valid(amount=amount)
