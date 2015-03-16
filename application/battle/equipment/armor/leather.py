from battle.equipment.armor import abstract


class Leather(abstract.AbstractArmor):
    instance = None

    @staticmethod
    def getArcheryProtection():
        return 5

    @staticmethod
    def getInstance():
        if Leather.instance is None:
            Leather.instance = Leather()

        return Leather.instance

