from . import Abstract
import models.Army.Domain

class Army_Collection(Abstract.AbstractCollection):
    domain = models.Army.Domain.Army_Domain
