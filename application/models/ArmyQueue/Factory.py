import models.Abstract.Factory

from . import Domain
from . import Mapper

from collection.ArmyQueueCollection import ArmyQueue_Collection


class ArmyQueue_Factory_Main(models.Abstract.Factory.Abstract_Factory):
    def get(self, _id):
        result = Mapper.ArmyQueue_Mapper.getById(_id)
        domain = Domain.ArmyQueue_Domain()
        domain.setOptions(result)

        return domain

    def load(self, town):
        result = Mapper.ArmyQueue_Mapper.load(town)
        collection = ArmyQueue_Collection()
        collection.setOptions(result)
        return collection

    def getDomainFromData(self, data):
        armyQueueDomain = Domain.ArmyQueue_Domain()

        armyQueueDomain.setUnit(data['unit'])
        armyQueueDomain.setTown(data['town'])
        armyQueueDomain.setCount(data['count'])
        armyQueueDomain.setCompleteAfter(data['complete_after'])
        armyQueueDomain.setStartAt(data['start_at'])
        armyQueueDomain.setQueueCode(data['queue_code'])

        return armyQueueDomain


ArmyQueue_Factory = ArmyQueue_Factory_Main()
