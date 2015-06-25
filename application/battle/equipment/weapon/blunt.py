from battle.equipment.weapon import abstract
from models.Equipment.Weapon import Common
from models.Equipment.Armor import Common as Armor_Common


class Blunt(abstract.AbstractWeapon):
    instance = None
    isMelee = True

    weaponType = Common.TYPE_BLUNT

    def _getModification(self, armorType):
        if armorType == Armor_Common.TYPE_ARMOR_MAIL:
            return 50
        elif armorType == Armor_Common.TYPE_ARMOR_LEATHER:
            return 10
        else:
            return 0

    @staticmethod
    def getInstance():
        if Blunt.instance is None:
            Blunt.instance = Blunt()

        return Blunt.instance
