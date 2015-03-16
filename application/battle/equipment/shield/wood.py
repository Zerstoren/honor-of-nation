from . import abstract

class Wood(abstract.AbstractShield):
    instance = None

    @staticmethod
    def getInstance():
        if Wood.instance is None:
            Wood.instance = Wood()

        return Wood.instance
