from battle.equipment.weapon import abstract
from models.Equipment.Weapon import Common
from models.Equipment.Armor import Common as Armor_Common


class Sword(abstract.AbstractWeapon):
    instance = None
    isMelee = True

    weaponType = Common.TYPE_SWORD

    def _getModification(self, armorType):
        if armorType == Armor_Common.TYPE_ARMOR_MAIL:
            return 0
        elif armorType == Armor_Common.TYPE_ARMOR_LEATHER:
            return 15
        else:
            return 15

    @staticmethod
    def getInstance():
        if Sword.instance is None:
            Sword.instance = Sword()

        return Sword.instance
