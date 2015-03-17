from battle.equipment.armor import abstract


class Plate(abstract.AbstractArmor):
    instance = None

    archeryArmorProtection = -5.0

    @staticmethod
    def getInstance():
        if Plate.instance is None:
            Plate.instance = Plate()

        return Plate.instance

