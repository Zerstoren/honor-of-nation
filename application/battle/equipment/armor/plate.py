from battle.equipment.armor import abstract
from models.Equipment.Armor import Common


class Plate(abstract.AbstractArmor):
    instance = None

    armorType = Common.TYPE_ARMOR_PLATE

    @staticmethod
    def getInstance():
        if Plate.instance is None:
            Plate.instance = Plate()

        return Plate.instance

