import helpers.MapCoordinate
from service.User import Service_User
from service.Town import Service_Town
from service.Equipment.Units import Service_Equipment_Units

from models.Army.Factory import Army_Factory

from helpers.mongo import objectId


class Decorate():
    def create(self, unit, town, count, user=None):
        town = Service_Town().getById(town)
        unit = Service_Equipment_Units().getForce(unit)
        count = int(count)

        return super().create(unit, town, count, user)

    def load(self, armyUser, position, config=None, user=None):
        armyUser = Service_User().decorate(Service_User.PARAMS).getUserDomain(armyUser)
        position = helpers.MapCoordinate.MapCoordinate(posId=int(position))

        return super().load(armyUser, position, config=config, user=user)

    def loadDetail(self, armyUser, _id, user=None):
        armyUser = Service_User().decorate(Service_User.PARAMS).getUserDomain(armyUser)

        return super().loadDetail(
            armyUser,
            objectId(_id),
            user
        )

    def move(self, general, path, user=None):
        return super().move(general, path, user)

    def changeMoveType(self, general, mode, user=None):
        return super().changeMoveType(general, mode, user)

    def addSuite(self, generalArmy, solidersArmy, user=None):
        generalDomain = Army_Factory.get(generalArmy)
        soliderDomain = Army_Factory.get(solidersArmy)
        return super().addSuite(generalDomain, soliderDomain, user)

    def removeSuite(self, generalArmy, solidersArmy, user=None):
        generalDomain = Army_Factory.get(generalArmy)
        soliderDomain = Army_Factory.get(solidersArmy)
        return super().removeSuite(generalDomain, soliderDomain, user)

    def addSolidersToGeneral(self, generalArmy, solidersCollection, user=None):
        solidersCollection = [objectId(i) for i in solidersCollection]
        domain = Army_Factory.get(generalArmy)
        collection = Army_Factory.getByIds(solidersCollection)
        return super().addSolidersToGeneral(domain, collection, user)

    def removeSolidersFromGeneral(self, generalArmy, solidersCollection, user=None):
        solidersCollection = [objectId(i) for i in solidersCollection]
        domain = Army_Factory.get(generalArmy)
        collection = Army_Factory.getByIds(solidersCollection)
        return super().removeSolidersFromGeneral(domain, collection, user)

    def moveInBuild(self, armyDomain, user=None):
        domain = Army_Factory.get(armyDomain)
        return super().moveInBuild(domain, user)

    def moveOutBuild(self, armyDomain, user=None):
        domain = Army_Factory.get(armyDomain)
        return super().moveOutBuild(domain, user)

    def merge(self, armyCollection, user=None):
        armyCollection = [objectId(i) for i in armyCollection]
        collection = Army_Factory.getByIds(armyCollection)
        return super().merge(collection, user)

    def split(self, armyDomain, size, user=None):
        domain = Army_Factory.get(armyDomain)
        size = int(size)
        return super().split(domain, size, user)

    def dissolution(self, armyDomain, user=None):
        domain = Army_Factory.get(armyDomain)
        return super().dissolution(domain, user)
