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

    def getByIds(self, ids):
        result = Mapper.Army_Mapper.getByIds(ids)
        armyCollection = Army_Collection()
        armyCollection.setOptions(result)

        return armyCollection

    def getByPosition(self, user, position, detail=False, inBuild=None):
        result = Mapper.Army_Mapper.getByPosition(user, position, detail=detail, inBuild=inBuild)
        armyCollection = Army_Collection()
        armyCollection.setOptions(result)

        return armyCollection

    def getSubGenerals(self, generalDomain):
        result = Mapper.Army_Mapper.getSubGenerals(generalDomain)
        armyCollection = Army_Collection()
        armyCollection.setOptions(result)

        return armyCollection

    def getCollectionByGeneral(self, generalDomain):
        result = Mapper.Army_Mapper.getByGeneral(generalDomain)
        armyCollection = Army_Collection()
        armyCollection.setOptions(result)

        return armyCollection

    def loadByMapCollection(self, collection):
        """
        :type collection: collection.MapCollection.Map_Collection
        """
        result = Mapper.Army_Mapper.getByPositions(collection)
        armyCollection = Army_Collection()
        armyCollection.setOptions(result)

        return armyCollection

Army_Factory = Army_Factory_Main()
