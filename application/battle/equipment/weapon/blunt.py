from battle.equipment.weapon import abstract


class Blunt(abstract.AbstractWeapon):
    instance = None
    isMelee = True

    @staticmethod
    def getInstance():
        if Blunt.instance is None:
            Blunt.instance = Blunt()

        return Blunt.instance
