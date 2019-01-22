from django.db import models


class Statement(models.Model):
    date_time = models.DateTimeField()
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=20)
    customer_id = models.CharField(max_length=20)

    @classmethod
    def get_transactions(cls, date_range):
        from_date = date_range["from_date"]
        to_date = date_range["to_date"]

        query_set = cls.objects.filter(date_time__range=(from_date, to_date))

        transactions = []

        for each in query_set:
            transactions.append(each.convert_to_dict())

        return transactions

    def convert_to_dict(self):
        return {
            "date_time": self.date_time,
            "amount": self.amount,
            "status": self.status,
            "customer_id": self.customer_id
        }
