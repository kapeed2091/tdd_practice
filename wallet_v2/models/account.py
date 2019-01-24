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
            cls.query_account_by_customer_id(customer_id)
            raise Exception
        except cls.DoesNotExist:
            account_id = cls.generate_account_id()
            account = cls.assign_account(customer_id, account_id)
        return account.get_account_dict()

    @classmethod
    def add_balance(cls, customer_id, amount):
        from wallet_v2.constants.general import TransactionType

        if cls.check_negative_amount(amount):
            raise Exception

        account = cls.get_account(customer_id)
        account.credit_balance(amount)
        cls.add_transaction(account_id=account.id, amount=amount,
                            transaction_type=TransactionType.CREDIT.value)
        return

    @classmethod
    def transfer_balance(
            cls, payee_customer_id, beneficiary_customer_id, amount):
        from wallet_v2.constants.general import TransactionType

        payee_account = cls.get_account(payee_customer_id)
        cls.validate_balance_transfer(
            payee_account, beneficiary_customer_id, amount)

        beneficiary_account = cls.get_account(beneficiary_customer_id)
        beneficiary_account.credit_balance(amount)
        cls.add_transaction(beneficiary_account.id, amount,
                            TransactionType.CREDIT.value)

        payee_account.debit_balance(amount)
        cls.add_transaction(payee_account.id, amount,
                            TransactionType.DEBIT.value)
        return

    @classmethod
    def query_account_by_customer_id(cls, customer_id):
        return cls.objects.get(customer_id=customer_id)

    @classmethod
    def generate_account_id(cls):
        import uuid
        return str(uuid.uuid4())[: cls.ACCOUNT_ID_LENGTH]

    @classmethod
    def assign_account(cls, customer_id, account_id):
        return cls.objects.create(customer_id=customer_id,
                                  account_id=account_id)

    def get_account_dict(self):
        # TODO: DOUBT: how to arrive at function name
        # when multiple formats aer expected
        return {
            'account_id': self.account_id,
            'customer_id': self.customer_id
        }

    @staticmethod
    def check_negative_amount(amount):
        if amount < 0:
            return True
        return False

    @classmethod
    def get_account(cls, customer_id):
        # TODO: DOUBT: G5 Vs G30
        # possibilities:
        # 1. rename get_account as validate_and_get_account
        # 2. return account as None if not exists and then raise exception
        try:
            account = cls.query_account_by_customer_id(customer_id)
            return account
        except cls.DoesNotExist:
            raise Exception("Customer does not exist")

    def credit_balance(self, amount):
        self.balance += amount
        self.save()

    @classmethod
    def add_transaction(cls, account_id, amount, transaction_type):
        from wallet_v2.models import Transaction
        Transaction.create_transaction(
            transaction_details={
                'account_id': account_id,
                'amount': amount,
                'transaction_type': transaction_type,
                'transaction_date': cls.get_now()
            })
        return

    @staticmethod
    def get_now():
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time
        return get_current_local_date_time()

    @classmethod
    def validate_balance_transfer(
            cls, payee_account, beneficiary_customer_id, amount):
        # TODO: DOUBT: 3 arguments to function / non-grouping of validations
        # and Inconsistency in arguments: payee_account, beneficiary_customer_id
        # TODO: DOUBT: will accessing payee_customer_id violate G34?
        payee_customer_id = payee_account.customer_id
        if cls.check_payee_and_beneficiary_accounts_are_same(
                payee_customer_id, beneficiary_customer_id):
            raise Exception("Payee and Beneficiary should not be same")

        if cls.check_positive_amount(amount):
            raise Exception("Transfer amount should be greater than zero")

        if payee_account.is_insufficient_balance(amount):
            raise Exception("Insufficient balance to transfer money")
        return

    @classmethod
    def check_payee_and_beneficiary_accounts_are_same(
            cls, payee_customer_id, beneficiary_customer_id):
        if payee_customer_id == beneficiary_customer_id:
            return True
        return False

    @staticmethod
    def check_positive_amount(amount):
        if amount <= 0:
            return True
        return False

    def is_insufficient_balance(self, amount):
        if self.balance < amount:
            return True
        return False

    def debit_balance(self, amount):
        self.balance -= amount
        self.save()

    @classmethod
    def get_balance(cls, customer_id):
        account = cls.get_account(customer_id)
        return account.balance
