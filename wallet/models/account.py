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
            from wallet.exceptions.exceptions import MultipleAccountsException
            from wallet.constants.exception_constants import MULTIPLE_ACCOUNTS
            raise MultipleAccountsException(MULTIPLE_ACCOUNTS)

        account_id = cls.generate_account_id(cls.ACCOUNT_ID_LENGTH)
        cls._assign_account_id_to_customer(
            account_id=account_id, customer_id=customer_id)

    @classmethod
    def transfer_amount_between_customers(cls, transaction_customer_details,
                                          amount):
        sender_customer_id = transaction_customer_details["sender_customer_id"]
        receiver_customer_id = transaction_customer_details[
            "receiver_customer_id"]

        sender_balance = cls.get_sender_balance(customer_id=sender_customer_id)

        cls.validate_amount(sender_balance=sender_balance, amount=amount)

        cls._deduct_balance_from_sender(
            customer_id=sender_customer_id, amount=amount
        )

        cls.add_balance_for_customer(
            customer_id=receiver_customer_id, amount=amount
        )

    @classmethod
    def add_balance_for_customer(cls, customer_id, amount):
        from wallet.exceptions.exceptions import NegativeAmountException, \
            NegativeAmountTransferException

        try:
            cls._validate_negative_amount(amount=amount)
        except NegativeAmountException:
            from wallet.constants.exception_constants import \
                NEGATIVE_AMOUNT_TRANSFER
            raise NegativeAmountTransferException(NEGATIVE_AMOUNT_TRANSFER)

        cls._add_account_balance(customer_id=customer_id, amount=amount)

    @classmethod
    def _deduct_balance_from_sender(cls, customer_id, amount):
        cls._validate_negative_amount(amount=amount)

        from wallet.exceptions.exceptions import NegativeAmountException, \
            NegativeAmountTransferException
        try:
            cls._deduct_account_balance(customer_id=customer_id,
                                        amount=amount)
        except NegativeAmountException:
            from wallet.constants.exception_constants import \
                NEGATIVE_AMOUNT_TRANSFER
            raise NegativeAmountTransferException(NEGATIVE_AMOUNT_TRANSFER)

    @classmethod
    def get_balance(cls, customer_id):
        account = cls.objects.get(customer_id=customer_id)
        return account.balance

    @classmethod
    def _check_if_customer_account_exists(cls, customer_id):
        return cls.objects.filter(customer_id=customer_id).exists()

    @staticmethod
    def generate_account_id(length):
        import uuid
        return str(uuid.uuid4())[0:length]

    @classmethod
    def _assign_account_id_to_customer(cls, account_id, customer_id):
        return cls.objects.create(
            account_id=account_id, customer_id=customer_id)

    @classmethod
    def _add_account_balance(cls, customer_id, amount):
        account = cls.get_account(customer_id)
        account.balance += amount
        account.save()

    @classmethod
    def _deduct_account_balance(cls, customer_id, amount):
        account = cls.get_account(customer_id)
        account.balance -= amount
        account.save()

    @staticmethod
    def is_negative_amount(amount):
        return amount < 0

    @classmethod
    def get_account(cls, customer_id):
        return cls.objects.get(customer_id=customer_id)

    @classmethod
    def get_sender_balance(cls, customer_id):
        try:
            sender_balance = cls.get_balance(
                customer_id=customer_id)
            return sender_balance
        except cls.DoesNotExist:
            from wallet.exceptions.exceptions import \
                InvalidSenderCustomerIdException
            from wallet.constants.exception_constants import \
                CUSTOMER_DOES_NOT_EXIST
            raise InvalidSenderCustomerIdException(CUSTOMER_DOES_NOT_EXIST)

    @classmethod
    def validate_amount(cls, sender_balance, amount):
        cls._validate_amount_type(amount=amount)

        cls._validate_insufficient_fund(
            balance=sender_balance, amount_comparator=amount
        )

        from wallet.exceptions.exceptions import NegativeAmountException, \
            NegativeAmountTransferException

        try:
            cls._validate_negative_amount(amount=amount)
        except NegativeAmountException:
            from wallet.constants.exception_constants import \
                NEGATIVE_AMOUNT_TRANSFER
            raise NegativeAmountTransferException(NEGATIVE_AMOUNT_TRANSFER)

    @staticmethod
    def _validate_amount_type(amount):
        if not isinstance(amount, int):
            from wallet.exceptions.exceptions import InvalidAmountTypeException
            from wallet.constants.exception_constants import \
                INVALID_AMOUNT_TYPE
            raise InvalidAmountTypeException(INVALID_AMOUNT_TYPE)

    @staticmethod
    def _validate_insufficient_fund(balance, amount_comparator):
        if balance < amount_comparator:
            from wallet.exceptions.exceptions import InsufficientFundException
            from wallet.constants.exception_constants import \
                INSUFFICIENT_FUND
            raise InsufficientFundException(INSUFFICIENT_FUND)

    @classmethod
    def _validate_negative_amount(cls, amount):
        if cls.is_negative_amount(amount):
            from wallet.exceptions.exceptions import NegativeAmountException
            from wallet.constants.exception_constants import NEGATIVE_AMOUNT
            raise NegativeAmountException(NEGATIVE_AMOUNT)
