from django.db import models


class Account(models.Model):
    CUSTOMER_ID_LENGTH = 20
    ACCOUNT_ID_LENGTH = 20
    customer_id = models.CharField(max_length=CUSTOMER_ID_LENGTH, unique=True)
    account_id = models.CharField(max_length=ACCOUNT_ID_LENGTH, unique=True)
    balance = models.IntegerField(default=0)

    @classmethod
    def create_account(cls, customer_id):
        cls._validate_customer_account_exists(customer_id)
        account_id = cls._generate_account_id()
        account = cls.assign_account(customer_id, account_id)
        return account._get_account_dict()

    @classmethod
    def add_balance(cls, customer_id, amount):
        from wallet_v2.constants.general import TransactionType

        if cls._check_negative_amount(amount):
            raise Exception

        account = cls.get_account(customer_id)
        account._credit_balance(amount)
        account._add_transaction(
            amount=amount, transaction_type=TransactionType.CREDIT.value)
        return

    @classmethod
    def transfer_balance(
            cls, payer_customer_id, beneficiary_customer_id, amount):
        from wallet_v2.constants.general import TransactionType

        payer_account = cls.get_account(payer_customer_id)
        payer_account._validate_balance_transfer(
            beneficiary_customer_id, amount)

        beneficiary_account = cls.get_account(beneficiary_customer_id)
        beneficiary_account._credit_balance(amount)
        beneficiary_account._add_transaction(
            amount, TransactionType.CREDIT.value)
        # TODO: move credit balance and add transaction into one function,
        # remove redundancy at add_balance

        payer_account._debit_balance(amount)
        payer_account._add_transaction(amount, TransactionType.DEBIT.value)
        return

    @classmethod
    def get_account(cls, customer_id):
        try:
            account = cls.objects.get(customer_id=customer_id)
            return account
        except cls.DoesNotExist:
            raise Exception("Customer does not exist")

    @classmethod
    def assign_account(cls, customer_id, account_id):
        return cls.objects.create(customer_id=customer_id,
                                  account_id=account_id)

    @classmethod
    def get_balance(cls, customer_id):
        account = cls.get_account(customer_id)
        return account.balance

    @classmethod
    def _validate_customer_account_exists(cls, customer_id):
        if cls.objects.filter(customer_id=customer_id).exists():
            raise Exception

    @classmethod
    def _generate_account_id(cls):
        import uuid
        return str(uuid.uuid4())[: cls.ACCOUNT_ID_LENGTH]

    def _get_account_dict(self):
        return {
            'account_id': self.account_id,
            'customer_id': self.customer_id
        }

    @staticmethod
    def _check_negative_amount(amount):
        return amount < 0

    def _credit_balance(self, amount):
        self.balance += amount
        self.save()

    def _add_transaction(self, amount, transaction_type):
        from wallet_v2.models import Transaction
        Transaction.create_transaction(
            transaction_details={
                'account_id': self.id,
                'amount': amount,
                'transaction_type': transaction_type,
                'transaction_date_time': self._get_now()
            })
        return

    @staticmethod
    def _get_now():
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time
        return get_current_local_date_time()

    def _validate_balance_transfer(
            self, beneficiary_customer_id, amount):
        if self._are_accounts_same(
                self.customer_id, beneficiary_customer_id):
            raise Exception("Payer and Beneficiary should not be same")

        if self._is_non_positive_amount(amount):
            raise Exception("Transfer amount should be greater than zero")

        if self._is_insufficient_balance(amount):
            raise Exception("Insufficient balance to transfer money")
        return

    @classmethod
    def _are_accounts_same(cls, payer_customer_id, beneficiary_customer_id):
        return payer_customer_id == beneficiary_customer_id

    @staticmethod
    def _is_non_positive_amount(amount):
        return amount <= 0

    def _is_insufficient_balance(self, amount):
        return self.balance < amount

    def _debit_balance(self, amount):
        self.balance -= amount
        self.save()
