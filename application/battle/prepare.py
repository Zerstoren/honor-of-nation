from collection.ArmyCollection import Army_Collection
from service.Army import Service_Army

from battle.structure.front import Front
from battle.structure.group import Group
from battle.structure.unit import Unit


class Prepare(object):
    def __init__(self, defenders, attackers):
        self.attackers = {
            Front.TYPE_AVANGARD: None,
            Front.TYPE_LEFT_FLANG: None,
            Front.TYPE_RIGHT_FLANG: None,
            Front.TYPE_REAR: None
        }

        self.defenders = {
            Front.TYPE_AVANGARD: None,
            Front.TYPE_LEFT_FLANG: None,
            Front.TYPE_RIGHT_FLANG: None,
            Front.TYPE_REAR: None
        }

        serviceArmy = Service_Army()

        self.defendersCollection = Army_Collection()
        for defender in defenders:
            for i in self.parseDetailLoad(serviceArmy.loadDetail(None, defender)):
                self.defendersCollection.append(i)

        self.attackersCollection =  Army_Collection()
        for attacker in attackers:
            for i in self.parseDetailLoad(serviceArmy.loadDetail(None, attacker)):
                print(i)
                self.attackersCollection.append(i)

        self.createFronts()

    def createFronts(self):
        self.attackers[Front.TYPE_AVANGARD] = self.getGroups(self.attackersCollection, Front.TYPE_AVANGARD, 'attack')

    def getGroups(self, unitsCollection, front, direction):
        for general, units in unitsCollection:
            if direction == 'attack' and general.getFormationAttack() == front:
                pass
            elif direction == 'defence' and general.getFormationDefence() == front:
                pass

    def getUnits(self):
        pass

    def parseDetailLoad(self, loads):
        def load(data):
            items = []

            general = loads['current']
            generalUnits = []

            if loads['suite']:
                generalUnits.append(loads['suite'])

            for i in loads['sub_army']:
                if not i['current'].getIsGeneral():
                    generalUnits.append(i['current'])
                else:
                    items += load(i)

            return [(general, generalUnits)] + items

        return load(loads)