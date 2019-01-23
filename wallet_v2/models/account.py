from django.db import models


class Account(models.Model):
    CUSTOMER_ID_LENGTH = 20
    ACCOUNT_ID_LENGTH = 20
    customer_id = models.CharField(max_length=CUSTOMER_ID_LENGTH, unique=True)
    account_id = models.CharField(max_length=ACCOUNT_ID_LENGTH, unique=True)
    balance = models.IntegerField(default=0)

    @classmethod
    def create_account(cls, customer_id):
        try:
            cls.objects.get(customer_id=customer_id)
            raise Exception
        except cls.DoesNotExist:
            account_id = cls.generate_account_id(cls.ACCOUNT_ID_LENGTH)
            account = cls.assign_account(customer_id, account_id)
        return {'customer_id': account.customer_id,
                'account_id': account.account_id}

    @staticmethod
    def generate_account_id(length):
        import uuid
        return str(uuid.uuid4())[: length]

    @classmethod
    def assign_account(cls, customer_id, account_id):
        return cls.objects.create(customer_id=customer_id,
                                  account_id=account_id)

    @classmethod
    def get_balance(cls, customer_id):
        account = cls.get_account(customer_id)
        return account.balance

    @classmethod
    def add_balance(cls, customer_id, amount):
        if cls.check_negative_amount(amount):
            raise Exception
        account = cls.get_account(customer_id)
        account.credit_balance(amount)
        return

    @staticmethod
    def check_negative_amount(amount):
        if amount < 0:
            return True
        return False

    def credit_balance(self, amount):
        self.balance += amount
        self.save()
        return self

    @classmethod
    def get_account(cls, customer_id):
        try:
            account = cls.objects.get(customer_id=customer_id)
            return account
        except cls.DoesNotExist:
            raise Exception("Customer does not exist")

    @classmethod
    def transfer_balance(
            cls, payee_customer_id, beneficiary_customer_id, amount):
        if amount <= 0:
            raise Exception("Transfer amount should be greater than zero")
        payee_account = cls.get_account(payee_customer_id)
        beneficiary_account = cls.get_account(beneficiary_customer_id)
        beneficiary_account.credit_balance(amount)
        payee_account.debit_balance(amount)
        return

    def debit_balance(self, amount):
        self.balance -= amount
        self.save()
        return self
