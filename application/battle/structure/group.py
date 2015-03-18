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
            if archer.steps >= 10:
                shoots = int(archer.steps / 10)
                archer.steps = archer.steps % 10

                for i in range(shoots):
                    group = targetFront.getRandomGroup()
                    if group.getCount() == 0:
                        break

                    target = group.getRandomUnit()

                    if Actions.archerFire(archer, target, bonus) and target.health <= 0:
                        group.removeUnit(target)

    def move(self):
        for unit in self.units:
            Actions.move(unit)

    def getRandomUnit(self):
        return self.units[ rand.randint(0, len(self.units) - 1) ]

    def getCount(self):
        return len(self.units)

    def getMeleeCount(self):
        return len(self.melee)

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
