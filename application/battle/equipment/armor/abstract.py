

class AbstractArmor(object):
    instance = None

    @staticmethod
    def getInstance():
        if AbstractArmor.instance is None:
            AbstractArmor.instance = AbstractArmor()

        return AbstractArmor.instance

    @staticmethod
    def getArcheryProtection():
        pass
