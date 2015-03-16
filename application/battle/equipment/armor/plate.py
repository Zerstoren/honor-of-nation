from battle.equipment.armor import abstract


class Plate(abstract.AbstractArmor):
    instance = None

    @staticmethod
    def getArcheryProtection():
        return 5

    @staticmethod
    def getInstance():
        if Plate.instance is None:
            Plate.instance = Plate()

        return Plate.instance

