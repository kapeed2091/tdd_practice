from django.db import models


class Transaction(models.Model):
    CUSTOMER_ID_LENGTH = 20
    TRANSACTION_ID_LENGTH = 20
    CHOICES_MAX_LENGTH = 20

    customer_id = models.CharField(max_length=CUSTOMER_ID_LENGTH)
    transaction_id = models.CharField(max_length=TRANSACTION_ID_LENGTH,
                                      unique=True)
    amount = models.IntegerField()
    type = models.CharField(max_length=CHOICES_MAX_LENGTH, choices=[
        ('Credit', 'Credit'), ('Debit', 'Debit')])

    @classmethod
    def get_statement(cls, customer_id):
        transactions =  list(cls.objects.filter(customer_id=customer_id))
        transactions_list = list()
        for transaction in transactions:
            transactions_list.append({
                'customer_id': transaction.customer_id,
                'transaction_id': transaction.transaction_id,
                'amount': transaction.amount,
                'type': transaction.type
            })
        return transactions_list

    @classmethod
    def add_transaction(cls, customer_id, amount, type):
        transaction_id = cls.generate_transaction_id(cls.TRANSACTION_ID_LENGTH)
        cls.assign_transaction_id(customer_id=customer_id,
                                  transaction_id=transaction_id, amount=amount,
                                  type=type)

    @classmethod
    def assign_transaction_id(cls, customer_id, transaction_id, amount, type):
        cls.objects.create(customer_id=customer_id,
                           transaction_id=transaction_id, amount=amount,
                           type=type)


    @staticmethod
    def generate_transaction_id(length):
        import uuid
        return str(uuid.uuid4())[0:length]
