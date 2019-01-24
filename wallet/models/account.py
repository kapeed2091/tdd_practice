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
        cls._raise_exception_for_customer_account_exists(customer_id)

        account_id = cls._generate_account_id()
        account = cls._assign_account_id_to_customer(
            account_id=account_id, customer_id=customer_id)

        return {'customer_id': account.customer_id,
                'account_id': account.account_id}

    @classmethod
    def transfer_amount(cls, source_customer_id, destination_customer_id,
                        transfer_amount):

        cls._raise_exception_for_insufficient_balance(
            customer_id=source_customer_id, amount=transfer_amount)

        try:
            cls.add_balance(customer_id=destination_customer_id,
                            amount=transfer_amount)

            cls._deduct_balance(customer_id=source_customer_id,
                                amount=transfer_amount)
        except Exception as exception:
            cls._raise_exception_for_failed_transfer_amount(exception)

    @classmethod
    def add_balance(cls, customer_id, amount):
        cls._raise_exception_for_invalid_amount(amount=amount)

        account = cls._get_account(customer_id)
        account._credit_amount(amount=amount)
        from wallet.constants.general import TransactionType
        account._add_transaction(amount=amount,
                                 transaction_type=TransactionType.CREDIT.value)

    @classmethod
    def get_balance(cls, customer_id):
        account = cls.objects.get(customer_id=customer_id)
        return account.balance

    @classmethod
    def raise_exception_for_invalid_customer(cls, customer_id):
        if cls._customer_does_not_exist(customer_id):
            from wallet.constants.exception_message import INVALID_CUSTOMER_ID
            raise Exception(INVALID_CUSTOMER_ID)

    @classmethod
    def _customer_does_not_exist(cls, customer_id):
        return not cls._customer_account_exists(customer_id=customer_id)

    @classmethod
    def _raise_exception_for_customer_account_exists(cls, customer_id):
        if cls._customer_account_exists(customer_id):
            from wallet.constants.exception_message import \
                ACCOUNT_ALREADY_EXISTS
            raise Exception(ACCOUNT_ALREADY_EXISTS)

    @classmethod
    def _customer_account_exists(cls, customer_id):
        return cls.objects.filter(customer_id=customer_id).exists()

    @classmethod
    def _generate_account_id(cls):
        import uuid
        return str(uuid.uuid4())[0:cls.ACCOUNT_ID_LENGTH]

    @classmethod
    def _assign_account_id_to_customer(cls, account_id, customer_id):
        return cls.objects.create(
            account_id=account_id, customer_id=customer_id)

    @classmethod
    def _raise_exception_for_insufficient_balance(cls, customer_id, amount):

        if cls._is_balance_insufficient_to_make_transfer(
                customer_id=customer_id, amount=amount):
            from wallet.constants.exception_message import \
                INSUFFICIENT_BALANCE_TO_MAKE_TRANSFER
            raise Exception(INSUFFICIENT_BALANCE_TO_MAKE_TRANSFER)

    @classmethod
    def _is_balance_insufficient_to_make_transfer(cls, customer_id, amount):
        balance = cls.get_balance(customer_id=customer_id)

        if balance >= amount:
            return False
        else:
            return True

    @classmethod
    def _get_account(cls, customer_id):
        try:
            return cls.objects.get(customer_id=customer_id)
        except cls.DoesNotExist:
            cls._raise_exception_for_invalid_customer_id()

    @staticmethod
    def _raise_exception_for_invalid_customer_id():
        from wallet.constants.exception_message import INVALID_CUSTOMER_ID
        raise Exception(INVALID_CUSTOMER_ID)

    def _credit_amount(self, amount):
        self.balance += amount
        self.save()

    @classmethod
    def _deduct_balance(cls, customer_id, amount):
        cls._raise_exception_for_invalid_amount(amount=amount)

        account = cls._get_account(customer_id)
        from wallet.constants.general import TransactionType
        account._add_transaction(amount=amount,
                                 transaction_type=TransactionType.DEBIT.value)
        account._debit_amount(amount=amount)

    def _add_transaction(self, amount, transaction_type):
        from wallet.models import Transaction

        message = \
            self._get_transaction_message(transaction_type=transaction_type)
        transaction_dict = {
            'account_id': self.id,
            'message': message,
            'amount': amount,
            'transaction_type': transaction_type
        }
        Transaction.add_transaction(transaction_dict=transaction_dict)

    @classmethod
    def _get_transaction_message(cls, transaction_type):
        from wallet.constants.general import TransactionType

        if transaction_type == TransactionType.DEBIT.value:
            return "Deducted the money"
        else:
            return "Added the money"

    def _debit_amount(self, amount):
        self.balance -= amount
        self.save()

    @classmethod
    def _raise_exception_for_invalid_amount(cls, amount):
        from wallet.constants.exception_message import \
            INVALID_AMOUNT_TO_ADD

        if cls._is_negative_amount(amount):
            raise Exception(INVALID_AMOUNT_TO_ADD)

        if cls._is_zero_amount(amount):
            raise Exception(INVALID_AMOUNT_TO_ADD)

        if cls._is_amount_type_int(amount):
            pass
        else:
            raise Exception(INVALID_AMOUNT_TO_ADD)

    @staticmethod
    def _is_negative_amount(amount):
        if amount < 0:
            return True
        return False

    @staticmethod
    def _is_zero_amount(amount):
        if amount == 0:
            return True
        return False

    @staticmethod
    def _is_amount_type_int(amount):
        return type(amount) == int

    @classmethod
    def _raise_exception_for_failed_transfer_amount(cls, exception):
        from wallet.constants.exception_message import \
            INVALID_AMOUNT_TO_TRANSFER
        from wallet.constants.exception_message import \
            INVALID_AMOUNT_TO_ADD
        from wallet.constants.exception_message import INVALID_CUSTOMER_ID

        error_code = exception.message[1]
        if error_code == INVALID_AMOUNT_TO_ADD[1]:
            raise Exception(INVALID_AMOUNT_TO_TRANSFER)

        if error_code == INVALID_CUSTOMER_ID[1]:
            raise Exception(INVALID_CUSTOMER_ID)




