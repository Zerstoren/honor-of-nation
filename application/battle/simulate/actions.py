from . import rand

class Actions(object):
    @staticmethod
    def move(unit):
        unit.steps += 1

        if unit.steps % unit.weapon_speed == 0:
            unit.attackReady = True

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

        shooter.attackReady = False
        if target.shield and rand.chance(target.shieldBlocking):
            target.shieldDurability -= shooter.damage

            if target.shieldDurability <= 0:
                target.shield = None
                target.shieldDurability = 0
                target.shieldBlocking = 0

            return False

        realDamage = Actions._getArcheryDamage(shooter, target, bonus)

        target.health -= realDamage

        return True

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

        result = round(shooter.damage * armorMod * defenceMod)

        if result >= shooter.damage * 1.5:
            result = 150
        elif result <= shooter.damage / 1.5:
            result = 50

        return result