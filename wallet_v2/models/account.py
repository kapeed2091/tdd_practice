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
        cls.add_credit_transaction(account_id=account.id, amount=amount,
                                   transaction_date=cls.get_now())
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

    @staticmethod
    def get_now():
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time
        return get_current_local_date_time()

    @classmethod
    def add_credit_transaction(cls, account_id, amount, transaction_date):
        from wallet_v2.models import Transaction
        from wallet_v2.constants.general import TransactionType
        Transaction.create_transaction(
            transaction_details={
                'account_id': account_id,
                'amount': amount,
                'transaction_type': TransactionType.CREDIT.value,
                'transaction_date': transaction_date
            })
        return

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

        payee_account = cls.get_account(payee_customer_id)
        cls.validate_balance_transfer(
            payee_account, beneficiary_customer_id, amount)

        beneficiary_account = cls.get_account(beneficiary_customer_id)
        beneficiary_account.credit_balance(amount)
        payee_account.debit_balance(amount)
        return

    @classmethod
    def validate_balance_transfer(
            cls, payee_account, beneficiary_customer_id, amount):
        payee_customer_id = payee_account.customer_id
        if cls.check_if_payee_and_beneficiary_accounts_are_same(
                payee_customer_id, beneficiary_customer_id):
            raise Exception("Payee and Beneficiary should not be same")

        if cls.check_amount_lte_zero(amount):
            raise Exception("Transfer amount should be greater than zero")

        if payee_account.check_if_insufficient_balance(amount):
            raise Exception("Insufficient balance to transfer money")
        return

    @staticmethod
    def check_amount_lte_zero(amount):
        if amount <= 0:
            return True
        return False

    def check_if_insufficient_balance(self, amount):
        if self.balance < amount:
            return True
        return False

    @classmethod
    def check_if_payee_and_beneficiary_accounts_are_same(
            cls, payee_customer_id, beneficiary_customer_id):
        if payee_customer_id == beneficiary_customer_id:
            return True
        return False

    def debit_balance(self, amount):
        self.balance -= amount
        self.save()
        return self
