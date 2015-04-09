from battle.structure.front import Front, FrontCollection

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

    def simulate(self):
        while True:
            for front in Front.TYPES[0:3]:
                self.attacker.getNextTarget(front, self.defender)
                self.defender.getNextTarget(front, self.attacker)

            for front in Front.TYPES[0:3]:
                self.attacker.get(front).move()
                self.defender.get(front).move()

            self.archeryFire()
            self.meleeAttack()

            if self.checkIsComplete():
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

            if front == Front.TYPE_AVANGARD:
                print("Attacker", frontAttacker.getUnitsCount())
                print("Defender", frontDefender.getUnitsCount())

            if frontDefender.getMeleeCount():
                frontDefender.meleeFire()

            if frontAttacker.getMeleeCount():
                frontAttacker.meleeFire()


    def checkIsComplete(self):
        if self.attacker.getArmySize() == 0:
            print("DEFENDER WIN")
            return True
        elif self.defender.getArmySize() == 0:
            print("ATTACKER WIN")
            return True

        return False