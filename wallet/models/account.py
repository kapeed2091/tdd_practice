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
        if cls._check_if_customer_account_exists(customer_id):
            raise Exception

        account_id = cls.generate_account_id(cls.ACCOUNT_ID_LENGTH)
        account = cls._assign_account_id_to_customer(
            account_id=account_id, customer_id=customer_id)

        return {'customer_id': account.customer_id,
                'account_id': account.account_id}

    @classmethod
    def _check_if_customer_account_exists(cls, customer_id):
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
    def transfer_amount_between_customers(cls, transaction_customer_details,
                                          amount):
        sender_customer_id = transaction_customer_details["sender_customer_id"]
        receiver_customer_id = transaction_customer_details[
            "receiver_customer_id"]

        try:
            sender_balance = cls.get_balance(
                customer_id=sender_customer_id)
        except cls.DoesNotExist:
            from wallet.exceptions.exceptions import \
                InvalidSenderCustomerIdException
            from wallet.constants.exception_constants import \
                CUSTOMER_DOES_NOT_EXIST
            raise InvalidSenderCustomerIdException(CUSTOMER_DOES_NOT_EXIST)

        cls._validate_amount_type(amount=amount)

        cls._validate_insufficient_fund(
            balance=sender_balance, amount_comparator=amount
        )

        from wallet.exceptions.exceptions import NegativeAmountException, \
            NegativeAmountTransferException
        try:
            cls.deduct_balance(customer_id=sender_customer_id,
                               amount=amount)
        except NegativeAmountException:
            from wallet.constants.exception_constants import \
                NEGATIVE_AMOUNT_TRANSFER
            raise NegativeAmountTransferException(NEGATIVE_AMOUNT_TRANSFER)

        cls.add_balance(customer_id=receiver_customer_id, amount=amount)

    @classmethod
    def deduct_balance(cls, customer_id, amount):
        if cls.is_negative_amount(amount):
            from wallet.exceptions.exceptions import NegativeAmountException
            from wallet.constants.exception_constants import NEGATIVE_AMOUNT
            raise NegativeAmountException(NEGATIVE_AMOUNT)

        account = cls.get_account(customer_id)
        account.balance -= amount
        account.save()

    @staticmethod
    def _validate_amount_type(amount):
        if not isinstance(amount, int):
            from wallet.exceptions.exceptions import InvalidAmountType
            from wallet.constants.exception_constants import \
                INVALID_AMOUNT_TYPE
            raise InvalidAmountType(INVALID_AMOUNT_TYPE)

    @staticmethod
    def _validate_insufficient_fund(balance, amount_comparator):
        if balance < amount_comparator:
            from wallet.exceptions.exceptions import InsufficientFund
            from wallet.constants.exception_constants import \
                INSUFFICIENT_FUND
            raise InsufficientFund(INSUFFICIENT_FUND)
