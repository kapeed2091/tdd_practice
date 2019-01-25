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
        cls.validate_account(customer_id=customer_id)

        account_id = cls.generate_account_id()
        account = cls.assign_account_id_to_customer(
            account_id=account_id, customer_id=customer_id)

        return account.convert_to_dict()

    @classmethod
    def add_balance(cls, customer_id, amount):
        cls.validate_amount(amount=amount)

        account = cls.get_account(customer_id)
        account.credit_balance(amount=amount)

    @classmethod
    def transfer_balance(cls, sender_customer_id, receiver_customer_id,
                         amount):
        cls.validate_amount(amount=amount)

        sender_account = cls.get_account(sender_customer_id)
        sender_account.validate_sender_balance(amount=amount)

        receiver_account = cls.get_account(receiver_customer_id)
        sender_account.are_same_accounts(
            receiver_account=receiver_account)

        sender_account.debit_balance(amount)
        receiver_account.credit_balance(amount)

    @classmethod
    def get_balance(cls, customer_id):
        account = cls.objects.get(customer_id=customer_id)
        return account.balance

    @classmethod
    def validate_account(cls, customer_id):
        if cls.customer_account_exists(customer_id):
            raise Exception('Customer Account already exists')

    @classmethod
    def generate_account_id(cls):
        import uuid
        return str(uuid.uuid4())[0:cls.ACCOUNT_ID_LENGTH]

    @classmethod
    def assign_account_id_to_customer(cls, account_id, customer_id):
        return cls.objects.create(
            account_id=account_id, customer_id=customer_id)

    def convert_to_dict(self):
        return {'customer_id': self.customer_id,
                'account_id': self.account_id}

    @classmethod
    def customer_account_exists(cls, customer_id):
        return cls.objects.filter(customer_id=customer_id).exists()

    @classmethod
    def validate_amount(cls, amount):
        if cls.is_non_positive(amount):
            raise Exception('Transfer balance cannot be zero or negative')

        if cls.is_non_int_type(amount):
            raise Exception('Transfer balance must be of type int')

    @classmethod
    def get_account(cls, customer_id):
        try:
            return cls.objects.get(customer_id=customer_id)
        except:
            raise Exception('Customer id doesnot exist')

    def validate_sender_balance(self, amount):
        if self.balance < amount:
            raise Exception(
                'Sender Balance should be more than transfer amount')

    def are_same_accounts(self, receiver_account):
        if self.account_id == receiver_account.account_id:
            raise Exception('Cannot transfer balance between same account')

    def credit_balance(self, amount):
        self.balance += amount
        self.save()

    def debit_balance(self, amount):
        self.balance -= amount
        self.save()

    @staticmethod
    def is_non_positive(amount):
        if amount <= 0:
            return True
        return False

    @staticmethod
    def is_non_int_type(amount):
        if type(amount) != int:
            return True
        return False
