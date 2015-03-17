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

    def simulate(self):
        for i in range(0, self.location.timeToAttack()):
            self.archeryFire()

    def archeryFire(self):
        target = self.attacker.getArcheryTarget()
        for front in self.defender.iterateAll():
            frontAttacker = self.attacker.get(front.getType())

            front.archersFire(target)
            frontAttacker.archersFire(front)

            frontAttacker.move()
            front.move()

        while True:
            for front in Front.TYPES[0:3]:
                frontAttackerTarget = self.attacker.getNextTarget(front, self.defender)
                frontDefenderTarget = self.defender.getNextTarget(front, self.attacker)
