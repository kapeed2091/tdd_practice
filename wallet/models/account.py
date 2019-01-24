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

        account_id = cls._generate_account_id(cls.ACCOUNT_ID_LENGTH)
        account = cls._assign_account_id_to_customer(
            account_id=account_id, customer_id=customer_id)

        return {'customer_id': account.customer_id,
                'account_id': account.account_id}

    @classmethod
    def add_balance(cls, customer_id, amount):
        if cls._is_negative(amount):
            raise Exception

        if cls._is_non_int_type(amount):
            raise Exception

        account = cls._get_account(customer_id)
        account._add_balance(amount=amount)

    @classmethod
    def transfer_balance(cls, sender_customer_id, receiver_customer_id,
                         amount):
        cls._validate_amount(amount=amount)

        sender_account = cls._get_account(sender_customer_id)
        sender_account._validate_sender_balance(amount=amount)

        receiver_account = cls._get_account(receiver_customer_id)
        sender_account._validate_unique_accounts(
            receiver_account=receiver_account)

        sender_account._deduct_balance(amount)
        receiver_account._add_balance(amount)

    @classmethod
    def get_balance(cls, customer_id):
        account = cls.objects.get(customer_id=customer_id)
        return account.balance

    @classmethod
    def _customer_account_exists(cls, customer_id):
        return cls.objects.filter(customer_id=customer_id).exists()

    @staticmethod
    def _generate_account_id(length):
        import uuid
        return str(uuid.uuid4())[0:length]

    @classmethod
    def _assign_account_id_to_customer(cls, account_id, customer_id):
        return cls.objects.create(
            account_id=account_id, customer_id=customer_id)

    @classmethod
    def _validate_amount(cls, amount):
        if cls._is_zero_or_negative(amount):
            raise Exception('Transfer balance cannot be zero or negative')

        if cls._is_non_int_type(amount):
            raise Exception('Transfer balance must be of type int')

    def _validate_sender_balance(self, amount):
        if self.balance < amount:
            raise Exception(
                'Sender Balance should be more than transfer amount')

    def _validate_unique_accounts(self, receiver_account):
        if self.account_id == receiver_account.account_id:
            raise Exception('Cannot transfer balance between same account')

    @staticmethod
    def _is_negative(amount):
        if amount < 0:
            return True
        return False

    @staticmethod
    def _is_non_int_type(amount):
        if type(amount) != int:
            return True
        return False

    @classmethod
    def _get_account(cls, customer_id):
        try:
            return cls.objects.get(customer_id=customer_id)
        except:
            raise Exception('Customer id doesnot exist')

    @staticmethod
    def _is_zero_or_negative(amount):
        if amount <= 0:
            return True
        return False

    def _deduct_balance(self, amount):
        self.balance -= amount
        self.save()

    def _add_balance(self, amount):
        self.balance += amount
        self.save()
