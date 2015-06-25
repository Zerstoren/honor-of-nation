from service.Army import Service_Army

from battle.structure.front import Front, FrontCollection
from battle.structure.group import Group
from battle.structure.unit import Unit

from battle.places.factory import PlacesFactory

class Prepare(object):
    def __init__(self, defenders, attackers):
        self.attackers = FrontCollection(inDefence=False)
        self.defenders = FrontCollection(inDefence=True)

        self.location = None

        serviceArmy = Service_Army()

        self.defendersCollection = []
        for defender in defenders:
            for i in self.parseDetailLoad(serviceArmy.loadDetail(None, defender)):
                self.defendersCollection += i

        self.attackersCollection = []
        for attacker in attackers:
            for i in self.parseDetailLoad(serviceArmy.loadDetail(None, attacker)):
                self.attackersCollection += i

        self.createFronts()
        self.getLocation(defenders[0])

        self.attackers.setLocation(self.location)
        self.defenders.setLocation(self.location)

    def getLocation(self, defender):
        armyDomain = Service_Army().get(defender)
        mapDomain = armyDomain.getMap()

        self.location = PlacesFactory.getPlace(mapDomain)

    def createFronts(self):
        self.attackers.setAvangard(self.getGroups(self.attackersCollection, Front.TYPE_AVANGARD, 'attack'))
        self.attackers.setLeftFlang(self.getGroups(self.attackersCollection, Front.TYPE_LEFT_FLANG, 'attack'))
        self.attackers.setRightFlang(self.getGroups(self.attackersCollection, Front.TYPE_RIGHT_FLANG, 'attack'))
        self.attackers.setRear(self.getGroups(self.attackersCollection, Front.TYPE_REAR, 'attack'))

        self.defenders.setAvangard(self.getGroups(self.defendersCollection, Front.TYPE_AVANGARD, 'defence'))
        self.defenders.setLeftFlang(self.getGroups(self.defendersCollection, Front.TYPE_LEFT_FLANG, 'defence'))
        self.defenders.setRightFlang(self.getGroups(self.defendersCollection, Front.TYPE_RIGHT_FLANG, 'defence'))
        self.defenders.setRear(self.getGroups(self.defendersCollection, Front.TYPE_REAR, 'defence'))

    def getGroups(self, unitsCollection, front, direction):
        front = Front(front)

        for general, units in unitsCollection:
            if (direction == 'attack' and general.getFormationAttack() == front) or \
                (direction == 'defence' and general.getFormationDefence() == front):

                group = Group()
                self.getUnits(general, units, group)
                front.addGroup(group)

        return front

    def getUnits(self, general, units, groupInstance):
        groupInstance.setGeneral(Unit(general))

        for unit in units:
            unitInstance = Unit(unit)

            for i in range(unit.getCount()):
                groupInstance.addUnit(unitInstance.cloneInstance())

    def parseDetailLoad(self, loads):
        items = []

        general = loads['current']
        generalUnits = []

        if loads['suite']:
            generalUnits.append(loads['suite'])

        for i in loads['sub_army']:
            if not i['current'].getIsGeneral():
                generalUnits.append(i['current'])
            else:
                items += self.parseDetailLoad(i)

        return [(general, generalUnits)] + items

    def export(self):
        return {
            'attacker': self.attackers,
            'defender': self.defenders,
            'location': self.location
        }