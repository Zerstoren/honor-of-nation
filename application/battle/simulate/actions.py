from . import rand

class Actions(object):
    @staticmethod
    def move(unit):
        unit.steps += unit.attackSpeed

    @staticmethod
    def archerFire(shooter, target, bonus):
        """
        :type shooter: battle.structure.unit.Unit
        :type target: battle.structure.unit.Unit
        :type bonus: int
        :type: bool
        """
        if rand.chance(Actions._getArcherChance(shooter, target, bonus)) is False:
            return False

        shooter.attackReady = False
        if target.shield and target.shield.gettingArcheryFire(shooter.damage, target):
            return False

        target.health -= Actions._getArcheryDamage(shooter, target)
        return True

    @staticmethod
    def _getArcherChance(shooter, target, bonus):
        clearChance = (10 + (shooter.agility - target.agility))
        if clearChance > 100:
            clearChance = 100
        elif clearChance <= 5:
            clearChance = 5

        return round(clearChance * bonus)

    @staticmethod
    def _getArcheryDamage(shooter, target):
        armorMod = target.armor.getArcheryArmorProtection()
        return round(shooter.damage / armorMod)
