from tests.unit.t_battle.generic import UnitTest_Battle_Generic
from battle.simulate.actions import Actions



class UnitTest_Battle_ActionsTest(UnitTest_Battle_Generic):

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

    def testArcherDamage(self):
        shooter = self.createUnit(weaponType=self.TYPE_WEAPON_BOW, damage=100, strength=100)
        target = self.createUnit(armorType=self.TYPE_ARMOR_LEATHER, absorption=60)

        self.assertEqual(
            Actions._getArcheryDamage(shooter, target, 1),
            116
        )