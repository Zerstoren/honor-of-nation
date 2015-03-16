from battle.equipment.weapon import abstract


class Sword(abstract.AbstractWeapon):
    instance = None
    isMelee = True

    @staticmethod
    def getInstance():
        if Sword.instance is None:
            Sword.instance = Sword()

        return Sword.instance
