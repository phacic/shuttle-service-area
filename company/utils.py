from enum import Enum
from django.db import models


class ChoiceBase(Enum):
    """ base class for model choice fields as Enum """

    @classmethod
    def to_list(cls):
        """ return a list of (name, value) which can be used as choice field in models"""
        return [(d.value, d.name) for d in cls]


class ActiveStatus(ChoiceBase):
    ACTIVE = 'A'
    INACTIVE = 'I'


class ActiveManager(models.Manager):
    """
    return only active objects (objects with status A)
    """
    def get_queryset(self):
        return super().get_queryset().filter(status=ActiveStatus.ACTIVE.value)
