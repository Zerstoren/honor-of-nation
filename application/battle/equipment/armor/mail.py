from battle.equipment.armor import abstract


class Mail(abstract.AbstractArmor):
    instance = None

    archeryArmorProtection = -5.0

    @staticmethod
    def getInstance():
        if Mail.instance is None:
            Mail.instance = Mail()

        return Mail.instance

