"""
Contains shared classes for storage adapters, including abstract base class.
"""

import abc


class DoesNotExist(Exception):
    """Exception to be raised when an entity is not found in storage."""
    pass


class Storage(abc.ABC):
    """Base class for storage adapters."""
    DoesNotExist = DoesNotExist

    @classmethod
    @abc.abstractmethod
    def create_bet(cls, *args, **kwargs):
        pass

    @classmethod
    @abc.abstractmethod
    def create_bet_participants(cls, *args, **kwargs):
        pass

    @classmethod
    @abc.abstractmethod
    def get_bet(cls, *args, **kwargs):
        pass

    @classmethod
    @abc.abstractmethod
    def get_bet_participants(cls, *args, **kwargs):
        pass