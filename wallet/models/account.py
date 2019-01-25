from django.db import models


class Account(models.Model):
    CUSTOMER_ID_LENGTH = 20
    ACCOUNT_ID_LENGTH = 20
    DEFAULT_BALANCE = 0
    MINIMUM_TRANSACTION_AMOUNT_SHOULD_BE_GREATER_THAN = 0

    customer_id = models.CharField(max_length=CUSTOMER_ID_LENGTH, unique=True)
    account_id = models.CharField(max_length=ACCOUNT_ID_LENGTH, unique=True)
    balance = models.IntegerField(default=DEFAULT_BALANCE)

    @classmethod
    def create_account(cls, customer_id):
        if cls._is_customer_account_exists(customer_id):
            raise Exception

        account_id = cls._generate_account_id(cls.ACCOUNT_ID_LENGTH)
        cls._create_account(
            account_id=account_id, customer_id=customer_id)

    def add_amount(self, amount):
        self._validate_amount_to_credit(amount)
        self._process_credit_amount(account=self, amount=amount)

    @classmethod
    def add_amount_with_customer_id(cls, customer_id, amount):
        pass

    @classmethod
    def transfer_amount(cls, sender_id, receiver_id, amount):
        sender_account = cls._get_sender_account(sender_id)
        receiver_account = cls._get_receiver_account(receiver_id)
        cls._validate_amount_to_transfer(sender_account=sender_account, amount=amount)
        cls._process_transfer_amount(sender_account=sender_account,
                                     receiver_account=receiver_account,
                                     amount=amount)

    @classmethod
    def get_balance(cls, customer_id):
        account = cls.objects.get(customer_id=customer_id)
        return account.balance

    @classmethod
    def get_account(cls, customer_id):
        return cls.objects.get(customer_id=customer_id)

    @classmethod
    def _is_customer_account_exists(cls, customer_id):
        return cls.objects.filter(customer_id=customer_id).exists()

    @staticmethod
    def _generate_account_id(length):
        import uuid
        return str(uuid.uuid4())[0:length]

    @classmethod
    def _create_account(cls, account_id, customer_id):
        # TODO: Rename function
        return cls.objects.create(
            account_id=account_id, customer_id=customer_id)

    def _validate_amount_to_credit(self, amount):
        self._validate_minimum_amount(amount)

    @classmethod
    def _get_sender_account(cls, sender_id):
        try:
            return cls.get_account(sender_id)
        except cls.DoesNotExist:
            raise Exception('Invalid sender id')

    @classmethod
    def _get_receiver_account(cls, receiver_id):
        try:
            return cls.get_account(receiver_id)
        except cls.DoesNotExist:
            raise Exception('Invalid receiver id')

    @classmethod
    def _validate_amount_to_transfer(cls, sender_account, amount):
        cls._validate_minimum_amount(amount)
        cls._validate_insufficient_balance(account=sender_account, amount=amount)

    @classmethod
    def _validate_minimum_amount(cls, amount):
        if amount <= cls.MINIMUM_TRANSACTION_AMOUNT_SHOULD_BE_GREATER_THAN:
            raise Exception('Invalid amount')

    @classmethod
    def _validate_insufficient_balance(cls, account, amount):
        if amount > account.balance:
            raise Exception('Insufficient balance')

    @classmethod
    def _process_transfer_amount(cls, sender_account, receiver_account, amount):
        cls._process_debit_amount(account=sender_account, amount=amount)
        cls._process_credit_amount(account=receiver_account, amount=amount)

    @classmethod
    def _process_debit_amount(cls, account, amount):
        from wallet.models import Transaction

        cls._debit_amount(account=account, amount=amount)
        Transaction.create_transaction(account=account, amount=-amount)

    @classmethod
    def _debit_amount(cls, account, amount):
        account.balance -= amount
        account.save()

    @classmethod
    def _process_credit_amount(cls, account, amount):
        from wallet.models import Transaction

        cls._credit_amount(account=account, amount=amount)
        Transaction.create_transaction(account=account, amount=amount)

    @classmethod
    def _credit_amount(cls, account, amount):
        account.balance += amount
        account.save()
