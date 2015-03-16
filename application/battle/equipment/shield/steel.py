from . import abstract

class Steel(abstract.AbstractShield):
    instance = None

    @staticmethod
    def getInstance():
        if Steel.instance is None:
            Steel.instance = Steel()

        return Steel.instance
