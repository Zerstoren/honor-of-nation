from battle.equipment.weapon import abstract


class Bow(abstract.AbstractWeapon):
    instance = None
    isMelee = False

    @staticmethod
    def getInstance():
        if Bow.instance is None:
            Bow.instance = Bow()

        return Bow.instance

