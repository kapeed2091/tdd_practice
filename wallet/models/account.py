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
    def add_balance(cls, customer_id, amount):
        if cls.is_negative_amount(amount):
            raise Exception

        if cls.is_non_int_type(amount):
            raise Exception

        account = cls.get_account(customer_id)
        account.balance += amount
        account.save()

    @staticmethod
    def is_negative_amount(amount):
        if amount < 0:
            return True
        return False

    @staticmethod
    def is_zero_or_negative_number(amount):
        if amount <= 0:
            return True
        return False

    @staticmethod
    def is_non_int_type(amount):
        if type(amount) != int:
            return True
        return False

    @classmethod
    def get_account(cls, customer_id):
        try:
            return cls.objects.get(customer_id=customer_id)
        except:
            raise Exception ('Customer id doesnot exist')

    @classmethod
    def transfer_balance(cls, sender_customer_id, receiver_customer_id, amount):
        if cls.is_zero_or_negative_number(amount):
            raise Exception ('Transfer balance cannot be zero or negative')

        if cls.is_non_int_type(amount):
            raise Exception ('Transfer balance must be of type int')

        sender_account = cls.get_account(sender_customer_id)
        if sender_account.balance < amount:
            raise Exception('Sender Balance should be more than transfer amount')

        receiver_account = cls.get_account(receiver_customer_id)
        if sender_account.account_id == receiver_account.account_id:
            raise Exception('Cannot transfer balance between same account')

        sender_account.balance = sender_account.balance - amount
        receiver_account.balance = receiver_account.balance + amount

        sender_account.save()
        receiver_account.save()
