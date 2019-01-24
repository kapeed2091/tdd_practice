"""
Created on 2019-01-24

@author: revanth
"""

import attr


class Entity():
    """
    Base class for all Topsy entities.

    Attaches attrs helper methods for convenience, and so that our business logic doesn't need to
    rely on attrs directly.
    """

    def replace(self, **kwargs):
        """Return new instance of this entity with updated field."""
        return attr.assoc(self, **kwargs)

    def asdict(self):
        """Return class attributes in a dictionary."""
        return attr.asdict(self)
