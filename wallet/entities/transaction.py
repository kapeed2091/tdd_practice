"""
Created on 2019-01-24

@author: revanth
"""
import attr
from .entity import Entity


@attr.s(frozen=True)
class Transaction(Entity):
    id = attr.ib()
    account_id = attr.ib()
    message = attr.ib()
    amount = attr.ib()
    transaction_type = attr.ib()

