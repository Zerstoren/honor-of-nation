import models.Abstract.Factory

from . import Domain
from . import Mapper

from collection.ArmyCollection import Army_Collection


class Army_Factory_Main(models.Abstract.Factory.Abstract_Factory):
    def get(self, _id):
        result = Mapper.Army_Mapper.getById(_id)
        domain = Domain.Army_Domain()
        domain.setOptions(result)

        return domain

    def getByPosition(self, user, position):
        result = Mapper.Army_Mapper.getByPosition(user, position)
        armyCollection = Army_Collection()
        armyCollection.setOptions(result)

        return armyCollection

Army_Factory = Army_Factory_Main()
