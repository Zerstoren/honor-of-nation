from battle.structure.front import Front

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
        for i in range(self.location.timeToConvergence()):
            self.archeryFire()

    def archeryFire(self):
        target = self.attacker.getArcheryTarget()
        for front in self.defender.iterateAll():
            front.archersFire(target)
