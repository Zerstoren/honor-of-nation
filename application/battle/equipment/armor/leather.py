from battle.equipment.armor import abstract


class Leather(abstract.AbstractArmor):
    instance = None

    archeryArmorProtection = -5.0

    @staticmethod
    def getInstance():
        if Leather.instance is None:
            Leather.instance = Leather()

        return Leather.instance

