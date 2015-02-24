from . import Abstract

from models.Town.Domain import Town_Domain

class Town_Collection(Abstract.AbstractCollection):
    domain = Town_Domain
