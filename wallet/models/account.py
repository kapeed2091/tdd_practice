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
        cls.raise_exception_for_customer_account_exists(customer_id)
        account_id = cls._generate_account_id()
        account = cls._assign_account_id_to_customer(
            account_id=account_id, customer_id=customer_id)

        return {'customer_id': account.customer_id,
                'account_id': account.account_id}

    @classmethod
    def raise_exception_for_customer_account_exists(cls, customer_id):
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
    def add_balance(cls, customer_id, amount):

        account = cls.get_account(customer_id)
        account.credit_amount(amount=amount)

    @classmethod
    def get_account(cls, customer_id):
        try:
            return cls.objects.get(customer_id=customer_id)
        except cls.DoesNotExist:
            cls._raise_exception_for_invalid_customer_id()

    @staticmethod
    def _raise_exception_for_invalid_customer_id():
        from wallet.constants.exception_message import INVALID_CUSTOMER_ID
        raise Exception(INVALID_CUSTOMER_ID)

    def credit_amount(self, amount):
        from wallet.models import Transaction

        self.raise_exception_for_invalid_amount(account=self, amount=amount)
        transaction_dict = {
            'account_id': self.id,
            'message': "added the money",
            'amount': amount,
            'transaction_type': "CREDIT"
        }
        Transaction.add_transaction(transaction_dict=transaction_dict)

        self.balance += amount
        self.save()

    @classmethod
    def deduct_balance(cls, customer_id, amount):
        account = cls.get_account(customer_id)
        account.debit_amount(amount=amount)

    def debit_amount(self, amount):
        self.raise_exception_for_invalid_amount(account=self, amount=amount)
        transaction_dict = {
            'account_id': self.id,
            'message': "deducted the money",
            'amount': amount,
            'transaction_type': "DEBIT"
        }
        from wallet.models import Transaction
        Transaction.add_transaction(transaction_dict=transaction_dict)

        self.balance -= amount
        self.save()

    @classmethod
    def raise_exception_for_invalid_amount(cls, account, amount):
        from wallet.constants.exception_message import \
            INVALID_AMOUNT_TO_ADD

        if account.is_negative_amount(amount):
            raise Exception(INVALID_AMOUNT_TO_ADD)

        if account.is_zero_amount(amount):
            raise Exception(INVALID_AMOUNT_TO_ADD)

        if account.is_amount_type_int(amount):
            pass
        else:
            raise Exception(INVALID_AMOUNT_TO_ADD)

    @staticmethod
    def is_negative_amount(amount):
        if amount < 0:
            return True
        return False

    @staticmethod
    def is_zero_amount(amount):
        if amount == 0:
            return True
        return False

    @staticmethod
    def is_amount_type_int(amount):
        return type(amount) == int

    @classmethod
    def transfer_amount(cls, source_customer_id, destination_customer_id,
                        transfer_amount):

        cls.raise_exception_for_insufficient_balance(
            customer_id=source_customer_id, amount=transfer_amount)

        try:
            cls.add_balance(customer_id=destination_customer_id,
                            amount=transfer_amount)

            cls.deduct_balance(customer_id=source_customer_id,
                               amount=transfer_amount)
        except Exception as e:
            from wallet.constants.exception_message import \
                INVALID_AMOUNT_TO_TRANSFER
            from wallet.constants.exception_message import \
                INVALID_AMOUNT_TO_ADD
            from wallet.constants.exception_message import INVALID_CUSTOMER_ID

            error_code = e.message[1]
            if error_code == INVALID_AMOUNT_TO_ADD[1]:
                raise Exception(INVALID_AMOUNT_TO_TRANSFER)

            if error_code == INVALID_CUSTOMER_ID[1]:
                raise Exception(INVALID_CUSTOMER_ID)

    @classmethod
    def raise_exception_for_insufficient_balance(cls, customer_id, amount):

        if cls.is_balance_sufficient_to_make_transfer(
                customer_id=customer_id, amount=amount):
            pass
        else:
            from wallet.constants.exception_message import \
                INSUFFICIENT_BALANCE_TO_MAKE_TRANSFER
            raise Exception(INSUFFICIENT_BALANCE_TO_MAKE_TRANSFER)

    @classmethod
    def is_balance_sufficient_to_make_transfer(cls, customer_id, amount):
        balance = cls.get_balance(customer_id=customer_id)

        if balance >= amount:
            return True
        else:
            return False

    @classmethod
    def get_balance(cls, customer_id):
        account = cls.objects.get(customer_id=customer_id)
        return account.balance



