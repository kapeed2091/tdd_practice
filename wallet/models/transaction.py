from django.db import models


class Transaction(models.Model):
    CUSTOMER_ID_LENGTH = 20
    TRANSACTION_ID_LENGTH = 20
    CHOICES_MAX_LENGTH = 20

    customer_id = models.CharField(max_length=CUSTOMER_ID_LENGTH)
    transaction_id = models.CharField(max_length=TRANSACTION_ID_LENGTH,
                                      unique=True)
    amount = models.IntegerField()
    transaction_type = models.CharField(max_length=CHOICES_MAX_LENGTH,choices=[
        ('Credit', 'Credit'), ('Debit', 'Debit')])

    @classmethod
    def get_statement(cls, customer_id):
        customer_transactions = cls._get_transactions(customer_id=customer_id)
        statement = cls.get_statement_from_transactions(
            transactions=customer_transactions)

        return statement

    @classmethod
    def add_transaction(cls, customer_id, amount,
                        transaction_type):
        transaction_id = cls.generate_transaction_id()
        cls.assign_transaction_id_to_customer(
            customer_id=customer_id, transaction_id=transaction_id,
            amount=amount, transaction_type=transaction_type)

    @classmethod
    def _get_transactions(cls, customer_id):
        return list(cls.objects.filter(customer_id=customer_id))

    @classmethod
    def get_statement_from_transactions(cls, transactions):
        statement = list()
        for transaction in transactions:
            statement.append({
                'customer_id': transaction.customer_id,
                'transaction_id': transaction.transaction_id,
                'amount': transaction.amount,
                'transaction_type': transaction.transaction_type
            })

        return statement

    @classmethod
    def generate_transaction_id(cls):
        import uuid
        return str(uuid.uuid4())[0:cls.TRANSACTION_ID_LENGTH]

    @classmethod
    def assign_transaction_id_to_customer(cls, customer_id, transaction_id,
                                          amount,
                                          transaction_type):
        cls.objects.create(customer_id=customer_id,
                           transaction_id=transaction_id,
                           amount=amount, transaction_type=transaction_type)
