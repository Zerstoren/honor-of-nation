from battle.simulate import rand

class AbstractShield(object):
    instance = None
    shieldBlocking = 1 # No action

    def tryBlocking(self, archerDamage, unit):
        """
        :param archerDamage: damage size
        :param unit: shield who get the archery damage
        :return: if false, shield not blocking damage, else blocking
        """
        if not rand.chance(unit.shieldBlocking):
            return False

        unit.shieldDurability -= round(archerDamage * self.shieldBlocking)

        if unit.shieldDurability <= 0:
            unit.shield = None
            unit.shieldDurability = 0
            unit.shieldBlocking = 0

        return True

    @staticmethod
    def getInstance():
        """
        :rtype: AbstractShield
        """
        if AbstractShield.instance is None:
            AbstractShield.instance = AbstractShield()

        return AbstractShield.instance

    @staticmethod
    def shieldArcheryProtection():
        pass

    @staticmethod
    def __bool__():
        return False