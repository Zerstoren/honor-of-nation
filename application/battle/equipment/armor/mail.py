from battle.equipment.armor import abstract


class Mail(abstract.AbstractArmor):
    instance = None

    @staticmethod
    def getArcheryProtection():
        return 5

    @staticmethod
    def getInstance():
        if Mail.instance is None:
            Mail.instance = Mail()

        return Mail.instance

