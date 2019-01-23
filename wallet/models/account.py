from django.db import models


class Account(models.Model):
    CUSTOMER_ID_LENGTH = 20
    ACCOUNT_ID_LENGTH = 20
    DEFAULT_BALANCE = 0

    customer_id = models.CharField(max_length=CUSTOMER_ID_LENGTH, unique=True)
    account_id = models.CharField(max_length=ACCOUNT_ID_LENGTH, unique=True)
    balance = models.IntegerField(default=DEFAULT_BALANCE)

    @classmethod
    def create_account(cls, customer_id):
        if cls._customer_account_exists(customer_id):
            raise Exception

        account_id = cls.generate_account_id(cls.ACCOUNT_ID_LENGTH)
        account = cls._assign_account_id_to_customer(
            account_id=account_id, customer_id=customer_id)

        return {'customer_id': account.customer_id,
                'account_id': account.account_id}

    @classmethod
    def _customer_account_exists(cls, customer_id):
        return cls.objects.filter(customer_id=customer_id).exists()

    @classmethod
    def _assign_account_id_to_customer(cls, account_id, customer_id):
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

    @classmethod
    def add_balance(cls, account, amount):
        from wallet.models import Transaction

        if cls.invalid_amount(amount):
            raise Exception('Invalid amount')

        account.balance += amount
        account.save()
        Transaction.create_obj(account=account, amount=amount)

    @classmethod
    def _remove_balance(cls, account, amount):
        if cls.invalid_amount(amount):
            raise Exception('Invalid amount')

        balance = account.balance
        if amount > balance:
            raise Exception('Insufficient balance')

        account.balance = balance - amount
        account.save()

    @staticmethod
    def invalid_amount(amount):
        if amount <= 0:
            return True
        return False

    @classmethod
    def get_account(cls, customer_id):
        return cls.objects.get(customer_id=customer_id)

    @classmethod
    def transfer_amount(cls, sender_id, receiver_id, amount):
        try:
            sender_account = cls.get_account(sender_id)
        except cls.DoesNotExist:
            raise Exception('Invalid sender id')

        try:
            receiver_account = cls.get_account(receiver_id)
        except cls.DoesNotExist:
            raise Exception('Invalid receiver id')

        cls._remove_balance(account=sender_account, amount=amount)
        print (receiver_account)
        cls.add_balance(account=receiver_account, amount=amount)
