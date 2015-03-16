from battle.simulate.actions import Actions
from battle.simulate import rand

class Group(object):
    def __init__(self):
        self.general = None
        self.units = []
        self.melee = []
        self.range = []

    def archersFire(self, targetFront, bonus):
        """
        :type targetFront: battle.structure.front.Front
        :return:
        """
        for archer in self.range:
            target = targetFront.getRandomGroup().getRandomUnit()
            Actions.archerFire(archer, target, bonus)

    def getRandomUnit(self):
        return self.units[ rand.randint(0, len(self.units) - 1) ]

    def getCount(self):
        return len(self.units)

    def setGeneral(self, general):
        self.general = general
        self.addUnit(general)

    def getGeneral(self):
        return self.general

    def addUnit(self, unit):
        if unit.weapon.isMelee:
            self.melee.append(unit)
        else:
            self.range.append(unit)

        self.units.append(unit)

    def getUnits(self):
        for unit in self.units:
            yield unit

    def getArchery(self):
        for unit in self.range:
            yield unit

    def getMelee(self):
        for unit in self.range:
            yield unit

    def removeUnit(self, unit):
        self.units.remove(unit)

        if unit.weapon.isMelee:
            self.melee.remove(unit)
        else:
            self.range.remove(unit)
