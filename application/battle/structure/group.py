from battle.simulate.actions import Actions
from battle.simulate import rand
from battle import log

import itertools

class Group(object):
    it = None

    def __init__(self):
        self.groupSize = 0
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
        log.group('`%s` %i archers fire for enemy `%s`' % (self.it, len(self.range), targetFront.it))

        for archer in self.range:
            if not archer.steps >= 10:
                continue

            shoots = int(archer.steps / 10)
            archer.steps %= 10

            log.unit('`%s` create archery shoots %i' % (archer.it, shoots))
            for i in range(shoots):
                group = targetFront.getRandomGroup()
                if group.getCount() == 0:
                    break

                target = group.getRandomUnit()

                log.unit('`%s` shoot to enemy `%s`' % (archer.it, target.it))
                if Actions.archerFire(archer, target, bonus) and target.health <= 0:
                    log.unit('`%s` archer killed enemy `%s`' % (archer.it, target.it))
                    group.removeUnit(target)

    def meleeAttack(self):
        targetGroup = self.getTarget()
        infinityGenerator = itertools.cycle(targetGroup.getUnits())

        for unit in self.getUnits():
            if not unit.steps >= 10:
                log.unit('`%s` skip step, he is weak')
                continue

            blows = int(unit.steps / 10)
            unit.steps %= 10

            log.unit('`%s` has blows %i' % (unit.it, blows))
            for blow in range(blows):
                target = None
                for i in range(targetGroup.getCount()):
                    tmp = next(infinityGenerator)
                    if targetGroup.hasUnit(tmp):
                        target = tmp
                        break

                if target is None:
                    log.group('`%s` killed enemy group `%s`' % (self.it, targetGroup.it))
                    self.removeTarget()
                    return

                log.unit('`%s` blow enemy `%s`' % (unit.it, target.it))
                if Actions.meleeFire(unit, target) and target.health <= 0:
                    targetGroup.removeUnit(target)
                    log.unit('`%s` infantry killed enemy `%s`' % (unit.it, target.it))

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
        self.groupSize += 1

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
        log.group('`%s` set melee target `%s`' % (self, self.target))

        if target and not target.getTarget():
            target.setTarget(self)

    def removeTarget(self):
        self.target = None
        log.group('`%s` remove target' % self.it)

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

    def __str__(self):
        return self.it