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
                self.attacker.get(front).move()
                self.defender.get(front).move()


            self.archeryFire()

            # for front in Front.TYPES[0:3]:
            #     # frontAttackerTarget = self.attacker.getNextTarget(front, self.defender)
            #     # frontDefenderTarget = self.defender.getNextTarget(front, self.attacker)

            if self.checkIsComplete():
                break

    def archeryFire(self):
        targetAttacker = self.attacker.getArcheryTarget()
        targetDefender = self.defender.getArcheryTarget()

        for front in Front.TYPES:
            frontAttacker = self.attacker.get(front)
            frontDefender = self.defender.get(front)


            s = self.attacker.getArmySize()
            frontDefender.archersFire(targetAttacker)
            print('attacker', s, self.attacker.getArmySize())

            s = self.defender.getArmySize()
            frontAttacker.archersFire(targetDefender)
            print('defender', s, self.defender.getArmySize())

    def checkIsComplete(self):
        if self.attacker.getArmySize() == 0:
            print("DEFENDER WIN")
            return True
        elif self.defender.getArmySize() == 0:
            print("ATTACKER WIN")
            return True

        return False