class Account(object):
    def __init__(self, id, customer_id, account_id, balance):
        self.id = id
        self.customer_id = customer_id
        self.account_id = account_id
        self.balance = balance