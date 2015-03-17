

class AbstractArmor(object):
    instance = None

    archeryArmorProtection = 0.0 # no mods

    def getArcheryArmorProtection(self):
        return (100.0 + self.archeryArmorProtection) / 100.0

    @staticmethod
    def getInstance():
        if AbstractArmor.instance is None:
            AbstractArmor.instance = AbstractArmor()

        return AbstractArmor.instance
