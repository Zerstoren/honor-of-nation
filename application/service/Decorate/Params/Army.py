import helpers.MapCoordinate
from service.User import Service_User
from service.Town import Service_Town
from service.Equipment.Units import Service_Equipment_Units

from models.Army.Factory import Army_Factory

from helpers.mongo import objectId

from exceptions.args import WrongArgumentType

import exceptions.args


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
        general = Army_Factory.get(general)
        mapPath = []
        for coordinate in path:
            try:
                x, y, direction = coordinate
            except ValueError:
                raise WrongArgumentType()

            mapPath.append({
                'pos_id': helpers.MapCoordinate.MapCoordinate(x=x, y=y).getPosId(),
                'direction': direction
            })

        return super().move(general, mapPath, user)

    def updatePathMove(self, general):
        general = Army_Factory.get(general)
        return super().updatePathMove(general)

    def changeMoveType(self, general, move, user=None):
        generalDomain = Army_Factory.get(general)
        move = int(move)

        if move not in [1,2,3,4]:
            raise exceptions.args.EnumError("Wrong move mode")

        return super().changeMoveType(generalDomain, move, user)

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
