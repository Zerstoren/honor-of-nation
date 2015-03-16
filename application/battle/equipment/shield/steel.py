from . import abstract

class Steel(abstract.AbstractShield):
    instance = None

    @staticmethod
    def shieldArcheryProtection():
        return 1.15

    @staticmethod
    def getInstance():
        if Steel.instance is None:
            Steel.instance = Steel()

        return Steel.instance

    @staticmethod
    def __bool__():
        return True