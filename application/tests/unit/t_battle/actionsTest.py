from tests.unit.t_battle.generic import UnitTest_Battle_Generic
from battle.simulate.actions import Actions


class UnitTest_Battle_ActionsTest(UnitTest_Battle_Generic):
    ### Actions.meleeFire
    def meleeFire(self):
        self.disableRandomChoice(True)
        shooter = self.createUnit(weaponType=self.TYPE_WEAPON_BOW, damage=100, agility=60)
        target = self.createUnit(armorType=self.TYPE_ARMOR_LEATHER, agility=30, health=500)

        self.assertTrue(Actions.meleeFire(shooter, target))
        self.assertEqual(target.health, 395)

    def testMeleeChanceNormal(self):
        attacker = self.createUnit(agility=100)
        defender = self.createUnit(agility=90)

        self.assertEqual(
            Actions._getMeleeChance(attacker, defender),
            60
        )

    def testMeleeChanceMinimal(self):
        attacker = self.createUnit(agility=0)
        defender = self.createUnit(agility=90)

        self.assertEqual(
            Actions._getMeleeChance(attacker, defender),
            10
        )

    def testMeleeChanceMaximal(self):
        attacker = self.createUnit(agility=100)
        defender = self.createUnit(agility=0)

        self.assertEqual(
            Actions._getMeleeChance(attacker, defender),
            90
        )


    def testMeleeDamageBow(self):
        attacker = self.createUnit(weaponType=self.TYPE_WEAPON_BOW, damage=100, agility=60)
        target = self.createUnit(armorType=self.TYPE_ARMOR_MAIL)

        self.assertEqual(
            Actions._getMeleeDamage(attacker, target),
            105
        )

    def testMeleeDamageBlunt(self):
        attacker = self.createUnit(weaponType=self.TYPE_WEAPON_BLUNT, damage=100, agility=60)
        target = self.createUnit(armorType=self.TYPE_ARMOR_MAIL)

        self.assertEqual(
            Actions._getMeleeDamage(attacker, target),
            150
        )

    def testMeleeDamageZeroSword(self):
        attacker = self.createUnit(weaponType=self.TYPE_WEAPON_SWORD, damage=100, agility=60)
        target = self.createUnit(armorType=self.TYPE_ARMOR_MAIL)

        self.assertEqual(
            Actions._getMeleeDamage(attacker, target),
            100
        )

    ### Actions.archerFire
    def testArcherFire(self):
        self.disableRandomChoice(True)
        shooter = self.createUnit(weaponType=self.TYPE_WEAPON_BOW, damage=100, agility=60)
        target = self.createUnit(armorType=self.TYPE_ARMOR_LEATHER, agility=30, health=500)

        self.assertTrue(Actions.archerFire(shooter, target, 1))
        self.assertEqual(target.health, 395)

    def testShieldDefenceArcherFire(self):
        self.disableRandomChoice(True)
        shooter = self.createUnit(weaponType=self.TYPE_WEAPON_BOW, damage=100, agility=60)
        target = self.createUnit(
            armorType=self.TYPE_ARMOR_LEATHER,
            shieldType=self.TYPE_SHIELD_WOOD,
            shieldDurability=1000,
            shieldBlocking=50,
            agility=30,
            health=500
        )

        Actions.archerFire(shooter, target, 1)

        self.assertEqual(target.shieldDurability, 900)

    ### Actions._getArcherChange
    def testArcherChange(self):
        shooter = self.createUnit(weaponType=self.TYPE_WEAPON_BOW, damage=100, agility=60)
        target = self.createUnit(armorType=self.TYPE_ARMOR_LEATHER, agility=30)

        self.assertEqual(
            Actions._getArcherChance(shooter, target, 1.3),
            52
        )

    def testMinimalArcherChange(self):
        shooter = self.createUnit(weaponType=self.TYPE_WEAPON_BOW, damage=100, agility=0)
        target = self.createUnit(armorType=self.TYPE_ARMOR_LEATHER, agility=30)

        self.assertEqual(
            Actions._getArcherChance(shooter, target, 1),
            5
        )

    def testMaximalArcherChange(self):
        shooter = self.createUnit(weaponType=self.TYPE_WEAPON_BOW, damage=100, agility=400)
        target = self.createUnit(armorType=self.TYPE_ARMOR_LEATHER, agility=0)

        self.assertEqual(
            Actions._getArcherChance(shooter, target, 1),
            100
        )

    ### Actions._getArcheryDamage
    def testArcherDamage(self):
        shooter = self.createUnit(weaponType=self.TYPE_WEAPON_BOW, damage=100, strength=100)
        target = self.createUnit(armorType=self.TYPE_ARMOR_LEATHER, absorption=60)

        self.assertEqual(
            Actions._getArcheryDamage(shooter, target),
            105
        )

    def testArcherCriticalDamage(self):
        shooter = self.createUnit(weaponType=self.TYPE_WEAPON_BOW, damage=100, criticalChance=100, criticalDamage=5)
        self.disableRandomChoice(True)

        self.assertEqual(
            Actions._getCriticalDamage(shooter, shooter.damage),
            500
        )

    def testArcherCriticalDamageNotChose(self):
        shooter = self.createUnit(weaponType=self.TYPE_WEAPON_BOW, damage=100, criticalChance=100, criticalDamage=5)
        self.disableRandomChoice(False)

        self.assertEqual(
            Actions._getCriticalDamage(shooter, shooter.damage),
            100
        )
