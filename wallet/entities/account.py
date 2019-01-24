"""
Created on 2019-01-24

@author: revanth
"""
import attr
from .entity import Entity


@attr.s(frozen=True)
class Account(Entity):
    id = attr.ib()
    customer_id = attr.ib()
    account_id = attr.ib()
    balance = attr.ib(default=0)
