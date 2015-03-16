

class AbstractShield(object):
    instance = None

    @staticmethod
    def getInstance():
        if AbstractShield.instance is None:
            AbstractShield.instance = AbstractShield()

        return AbstractShield.instance

    @staticmethod
    def shieldArcheryProtection():
        pass

    @staticmethod
    def __bool__():
        return False