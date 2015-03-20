

class AbstractArmor(object):
    instance = None
    armorType = None

    def getType(self):
        return self.armorType

    @staticmethod
    def getInstance():
        if AbstractArmor.instance is None:
            AbstractArmor.instance = AbstractArmor()

        return AbstractArmor.instance
