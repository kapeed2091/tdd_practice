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

        account = cls.get_account(customer_id)
        account.balance += amount
        account.save()

    @staticmethod
    def is_negative_amount(amount):
        if amount < 0:
            return True
        return False

    @classmethod
    def get_account(cls, customer_id):
        return cls.objects.get(customer_id=customer_id)

    @classmethod
    def transfer_money(cls, customer_id, beneficiary_customer_id, amount):
        account = cls.get_account(customer_id)
        beneficiary_account = cls.get_account(beneficiary_customer_id)

        cls.validate_amount_to_transfer(amount=amount)
        if account.is_sufficient_balance_to_transfer(transfer_amount=amount):
            cls.debit_balance(account, amount)
            cls.credit_balance(beneficiary_account, amount)
        else:
            raise Exception
        return

    @staticmethod
    def validate_amount_to_transfer(amount):
        if amount <= 0:
            raise Exception

    def is_sufficient_balance_to_transfer(self, transfer_amount):
        if self.balance < transfer_amount:
            return False
        else:
            return True

    def credit_balance(self, amount):
        self.balance += amount
        self.save()

    def debit_balance(self, amount):
        self.balance -= amount
        self.save()
