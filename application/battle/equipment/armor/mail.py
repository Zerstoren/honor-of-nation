from battle.equipment.armor import abstract
from models.Equipment.Armor import Common


class Mail(abstract.AbstractArmor):
    instance = None

    armorType = Common.TYPE_ARMOR_MAIL

    @staticmethod
    def getInstance():
        if Mail.instance is None:
            Mail.instance = Mail()

        return Mail.instance

