from battle.equipment.weapon import abstract


class Spear(abstract.AbstractWeapon):
    instance = None
    isMelee = True

    @staticmethod
    def getInstance():
        if Spear.instance is None:
            Spear.instance = Spear()

        return Spear.instance
