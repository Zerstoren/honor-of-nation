import helpers.MapCoordinate
from service.User import Service_User
from service.Town import Service_Town
from service.Equipment.Units import Service_Equipment_Units


class Decorate():
    def create(self, unit, town, count, user=None):
        town = Service_Town().getById(town)
        unit = Service_Equipment_Units().getForce(unit)
        count = int(count)

        return super().create(unit, town, count, user)

    def load(self, armyUser, position, user=None):
        armyUser = Service_User().decorate(Service_User.PARAMS).getUserDomain(armyUser)
        position = helpers.MapCoordinate.MapCoordinate(posId=int(position))

        return super().load(armyUser, position, user)
