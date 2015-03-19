from . import abstract

class Wood(abstract.AbstractShield):
    instance = None

    shieldBlocking = 1

    @staticmethod
    def getInstance():
        if Wood.instance is None:
            Wood.instance = Wood()

        return Wood.instance

    @staticmethod
    def __bool__():
        return True