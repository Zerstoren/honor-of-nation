import models.Abstract.Factory

from . import Domain
from . import Mapper

from collection.ArmyCollection import Army_Collection


class Army_Factory_Main(models.Abstract.Factory.Abstract_Factory):
    def _getCollectionFromData(self, data):
        armyCollection = Army_Collection()
        armyCollection.setOptions(data)

        return armyCollection

    def get(self, _id):
        result = Mapper.Army_Mapper.getById(_id)
        domain = Domain.Army_Domain()
        domain.setOptions(result)

        return domain

    def getByIds(self, ids):
        result = Mapper.Army_Mapper.getByIds(ids)
        return self._getCollectionFromData(result)

    def getByPosition(self, user, position, detail=False, inBuild=None):
        result = Mapper.Army_Mapper.getByPosition(user, position, detail=detail, inBuild=inBuild)
        return self._getCollectionFromData(result)

    def getSubGenerals(self, generalDomain):
        result = Mapper.Army_Mapper.getSubGenerals(generalDomain)
        return self._getCollectionFromData(result)

    def getCollectionByGeneral(self, generalDomain):
        result = Mapper.Army_Mapper.getByGeneral(generalDomain)
        return self._getCollectionFromData(result)

    def loadByMapCollection(self, collection):
        """
        :type collection: collection.MapCollection.Map_Collection
        """
        result = Mapper.Army_Mapper.getByPositions(collection)
        return self._getCollectionFromData(result)

    def loadByMapCollectionWithoutUser(self, user, collection):
        result = Mapper.Army_Mapper.getByMapCollectionWithoutUser(user, collection)
        return self._getCollectionFromData(result)

Army_Factory = Army_Factory_Main()
