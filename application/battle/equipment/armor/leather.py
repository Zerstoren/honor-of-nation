from battle.equipment.armor import abstract
from models.Equipment.Armor import Common


class Leather(abstract.AbstractArmor):
    instance = None

    armorType = Common.TYPE_ARMOR_LEATHER

    @staticmethod
    def getInstance():
        if Leather.instance is None:
            Leather.instance = Leather()

        return Leather.instance

