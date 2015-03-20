from battle.equipment.weapon import abstract
from models.Equipment.Weapon import Common
from models.Equipment.Armor import Common as Armor_Common


class Bow(abstract.AbstractWeapon):
    instance = None
    isMelee = False

    weaponType = Common.TYPE_BOW

    def _getModification(self, armorType):
        if armorType == Armor_Common.TYPE_ARMOR_MAIL:
            return 5
        elif armorType == Armor_Common.TYPE_ARMOR_LEATHER:
            return 5
        else:
            return 5

    @staticmethod
    def getInstance():
        if Bow.instance is None:
            Bow.instance = Bow()

        return Bow.instance

