from . import Abstract
import models.ArmyQueue.Domain

class ArmyQueue_Collection(Abstract.AbstractCollection):
    domain = models.ArmyQueue.Domain.ArmyQueue_Domain
