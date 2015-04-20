from battle.structure.front import Front
from exceptions import battle as battleExceptions

from battle import log


class Battle(object):
    attacker = None
    defender = None
    location = None

    def importData(self, attacker, defender, location):
        """
        :type attacker: battle.structure.front.FrontCollection
        :type defender: battle.structure.front.FrontCollection
        :type location: battle.places.abstract.AbstractPlace
        """
        self.attacker = attacker
        self.defender = defender
        self.location = location

        self.attacker.setLocation(location)
        self.defender.setLocation(location)

        self.attacker.it = 'attacker'
        self.defender.it = 'defender'

        self.attacker.get(Front.TYPE_AVANGARD).it = 'attacker_avangard'
        self.attacker.get(Front.TYPE_LEFT_FLANG).it = 'attacker_left_flang'
        self.attacker.get(Front.TYPE_RIGHT_FLANG).it = 'attacker_right_flang'
        self.attacker.get(Front.TYPE_REAR).it = 'attacker_rear'

        self.defender.get(Front.TYPE_AVANGARD).it = 'defender_avangard'
        self.defender.get(Front.TYPE_LEFT_FLANG).it = 'defender_left_flang'
        self.defender.get(Front.TYPE_RIGHT_FLANG).it = 'defender_right_flang'
        self.defender.get(Front.TYPE_REAR).it = 'defender_rear'

        for direction in Front.TYPES:
            i = 1
            for group in self.attacker.get(direction).getGroups():
                group.it = self.attacker.get(direction).it + ('_group_%i' % i)

                y = 1
                for unit in group.getUnits():
                    unit.it = group.it + '_unit_%s' % y
                    y += 1

                i += 1

            i = 1
            for group in self.defender.get(direction).getGroups():
                group.it = self.defender.get(direction).it + ('_group_%i' % i)

                y = 1
                for unit in group.getUnits():
                    unit.it = group.it + '_unit_%s' % y
                    y += 1

                i += 1

        log.battle('INFORMATION ABOUT LOAD DATA')

        for direction in Front.TYPES:
            front = self.attacker.get(direction)
            log.front('%s front' % front.it)

            for group in front.getGroups():
                log.group('%s group' % group.it)

                if group.general:
                    log.unit('%s general with id %s' % (group.it, group.general.it))

                for unit in group.getUnits():
                    log.unit('%s unit with id %s' % (unit.it, unit._id))

        for direction in Front.TYPES:
            front = self.defender.get(direction)
            log.front('%s front' % front.it)

            for group in front.getGroups():
                log.group('%s group' % group.it)

                if group.general:
                    log.unit('%s general with id %s' % (group.it, group.general.it))

                for unit in group.getUnits():
                    log.unit('%s unit with id %s' % (unit.it, unit._id))


    def simulate(self):
        i = 0

        while True:
            i += 1
            log.battle('Start round %i' % i)

            for front in Front.TYPES:
                self.attacker.getNextTarget(front, self.defender)
                self.defender.getNextTarget(front, self.attacker)

            for front in Front.TYPES:
                self.attacker.get(front).move()
                self.defender.get(front).move()

            self.archeryFire()
            self.meleeAttack()

            if self.checkIsComplete():
                break

            if i == 100:
                break

    def archeryFire(self):
        targetAttacker = self.attacker.getArcheryTarget()
        targetDefender = self.defender.getArcheryTarget()

        for front in Front.TYPES:
            frontAttacker = self.attacker.get(front)
            frontDefender = self.defender.get(front)

            if frontDefender.getRangeCount():
                frontDefender.archersFire(targetAttacker)

            if frontAttacker.getRangeCount():
                frontAttacker.archersFire(targetDefender)

    def meleeAttack(self):
        for front in Front.TYPES:
            frontAttacker = self.attacker.get(front)
            frontDefender = self.defender.get(front)

            if frontDefender.getMeleeCount():
                try:
                    frontDefender.meleeFire()
                except battleExceptions.EnemyFrontIsDeath:
                    pass

            if frontAttacker.getMeleeCount():
                try:
                    frontAttacker.meleeFire()
                except battleExceptions.EnemyFrontIsDeath:
                    pass

    def checkIsComplete(self):
        if self.attacker.getArmySize() == 0:
            log.battle("DEFENDER WIN")
            return True
        elif self.defender.getArmySize() == 0:
            log.battle("ATTACKER WIN")
            return True

        return False