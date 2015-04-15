from battle.simulate.actions import Actions
from battle.simulate import rand

import itertools

class Group(object):
    def __init__(self):
        self.general = None
        self.units = []
        self.melee = []
        self.range = []
        self.target = None

    def archersFire(self, targetFront, bonus):
        """
        :type targetFront: battle.structure.front.Front
        :return:
        """
        for archer in self.range:
            if not archer.steps >= 10:
                continue

            shoots = int(archer.steps / 10)
            archer.steps %= 10

            for i in range(shoots):
                group = targetFront.getRandomGroup()
                if group.getCount() == 0:
                    break

                target = group.getRandomUnit()

                if Actions.archerFire(archer, target, bonus) and target.health <= 0:
                    group.removeUnit(target)

    def meleeAttack(self):
        group = self.getTarget()
        infinityGenerator = itertools.cycle(group.getUnits())

        for unit in self.getUnits():
            tmp = None
            target = None

            for i in range(len(group.getUnits())):
                tmp = next(infinityGenerator)

                if group.hasUnit(tmp):
                    target = tmp

            if target is None:
                break

            if Actions.meleeFire(unit, target) and target.health <= 0:
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

    def getRangeCount(self):
        return len(self.range)

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

    def getTarget(self):
        """
        :rtype: Group
        """
        return self.target

    def setTarget(self, target):
        self.target = target
        if not target.getTarget():
            target.setTarget(self)

    def getUnits(self):
        return self.units

    def hasUnit(self, unit):
        return unit in self.units

    def getArchery(self):
        return self.range

    def getMelee(self):
        return self.melee

    def removeUnit(self, unit):
        self.units.remove(unit)

        if unit.weapon.isMelee:
            self.melee.remove(unit)
        else:
            self.range.remove(unit)
