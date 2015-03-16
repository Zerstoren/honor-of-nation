from . import rand

class Actions(object):
    @staticmethod
    def archerFire(shooter, target, bonus):
        """
        :type shooter: battle.structure.unit.Unit
        :type target: battle.structure.unit.Unit
        :type bonus: int
        :type: bool
        """
        if rand.chance(Actions._getArcherChange(shooter, target, bonus)) is False:
            return False

        realDamage = Actions._getArcheryDamage(shooter, target, bonus)

    @staticmethod
    def _getArcherChange(shooter, target, bonus):
        clearChance = (10 + (shooter.agility - target.agility))
        if clearChance > 100:
            clearChance = 100
        elif clearChance <= 5:
            clearChance = 5

        return round(clearChance * bonus)

    @staticmethod
    def _getArcheryDamage(shooter, target, bonus):
        armorMod = (100 + target.armor.getArcheryProtection()) / 100
        defenceMod = ((100 - ((target.absorption - shooter.strength) / 4)) / 100) * bonus

        return round(shooter.damage * armorMod * defenceMod)