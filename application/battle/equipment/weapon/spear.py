from battle.equipment.weapon import abstract
from models.Equipment.Weapon import Common
from models.Equipment.Armor import Common as Armor_Common


class Spear(abstract.AbstractWeapon):
    instance = None
    isMelee = True

    weaponType = Common.TYPE_SPEAR

    def _getModification(self, armorType):
        if armorType == Armor_Common.TYPE_ARMOR_MAIL:
            return 0
        elif armorType == Armor_Common.TYPE_ARMOR_LEATHER:
            return 0
        else:
            return 10

    @staticmethod
    def getInstance():
        if Spear.instance is None:
            Spear.instance = Spear()

        return Spear.instance
