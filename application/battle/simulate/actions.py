from . import rand

class Actions(object):
    @staticmethod
    def move(unit):
        unit.steps += unit.attackSpeed
        unit.absorption -= 1

    @staticmethod
    def meleeFire(unit, target):
        """
        :type unit: battle.structure.unit.Unit
        :type target: battle.structure.unit.Unit
        """

        if rand.chance(Actions._getMeleeChance(unit, target)) is False:
            return False

        unit.attackReady = False
        if target.shield and target.shield.tryBlocking(unit.damage, target):
            return False

    @staticmethod
    def _getMeleeChance(unit, target):
        chance = (50 + (unit.agility - target.agility))
        if chance > 90:
            chance = 90
        elif chance <= 10:
            chance = 10

        return chance

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
        if target.shield and target.shield.tryBlocking(shooter.damage, target):
            return False

        damage = Actions._getArcheryDamage(shooter, target)
        damage = Actions._getCriticalDamage(shooter, damage)

        target.health -= damage
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

    @staticmethod
    def _getCriticalDamage(shooter, damage):
        if rand.chance(shooter.criticalChance):
            damage = round(damage * shooter.criticalDamage)

        return damage
