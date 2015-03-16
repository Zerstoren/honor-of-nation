from tests.unit.t_battle.generic import UnitTest_Battle_Generic
from battle.simulate.actions import Actions



class UnitTest_Battle_ActionsTest(UnitTest_Battle_Generic):
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
            Actions._getArcherChange(shooter, target, 1.3),
            52
        )

    def testMinimalArcherChange(self):
        shooter = self.createUnit(weaponType=self.TYPE_WEAPON_BOW, damage=100, agility=0)
        target = self.createUnit(armorType=self.TYPE_ARMOR_LEATHER, agility=30)

        self.assertEqual(
            Actions._getArcherChange(shooter, target, 1),
            5
        )

    def testMaximalArcherChange(self):
        shooter = self.createUnit(weaponType=self.TYPE_WEAPON_BOW, damage=100, agility=400)
        target = self.createUnit(armorType=self.TYPE_ARMOR_LEATHER, agility=0)

        self.assertEqual(
            Actions._getArcherChange(shooter, target, 1),
            100
        )

    ### Actions._getArcheryDamage
    def testArcherDamage(self):
        shooter = self.createUnit(weaponType=self.TYPE_WEAPON_BOW, damage=100, strength=100)
        target = self.createUnit(armorType=self.TYPE_ARMOR_LEATHER, absorption=60)

        self.assertEqual(
            Actions._getArcheryDamage(shooter, target, 1),
            116
        )

    def testMinimalArcherDamage(self):
        shooter = self.createUnit(weaponType=self.TYPE_WEAPON_BOW, damage=100, strength=0)
        target = self.createUnit(armorType=self.TYPE_ARMOR_LEATHER, absorption=300)

        self.assertEqual(
            Actions._getArcheryDamage(shooter, target, 1),
            50
        )

    def testMaximalArcherDamage(self):
        shooter = self.createUnit(weaponType=self.TYPE_WEAPON_BOW, damage=100, strength=300)
        target = self.createUnit(armorType=self.TYPE_ARMOR_LEATHER, absorption=0)

        self.assertEqual(
            Actions._getArcheryDamage(shooter, target, 1),
            150
        )
