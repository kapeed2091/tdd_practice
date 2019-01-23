from django.db import models


class Statement(models.Model):
    date_time = models.DateTimeField()
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=20)
    customer_id = models.CharField(max_length=20)

    @classmethod
    def get_transactions(cls, customer_id, date_range):
        cls._date_range_validation(date_range=date_range)

        date_range_tuple = cls._get_date_range_tuple(date_range=date_range)
        query_set = cls.objects.filter(
            customer_id=customer_id, date_time__range=date_range_tuple
        )

        transactions = []
        for each in query_set:
            transactions.append(each.convert_to_dict())

        return transactions

    @staticmethod
    def _date_range_validation(date_range):
        from_date = date_range["from_date"]
        to_date = date_range["to_date"]

        if from_date > to_date:
            from wallet.exceptions.exceptions import InvalidDateRangeException
            from wallet.constants.exception_constants import INVALID_DATE_RANGE
            raise InvalidDateRangeException(INVALID_DATE_RANGE)

    @staticmethod
    def _get_date_range_tuple(date_range):
        return date_range["from_date"], date_range["to_date"]

    def convert_to_dict(self):
        return {
            "date_time": self.date_time,
            "amount": self.amount,
            "status": self.status,
            "customer_id": self.customer_id
        }
