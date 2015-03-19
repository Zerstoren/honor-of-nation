from tests.unit.t_battle.generic import UnitTest_Battle_Generic

from battle.equipment.shield.abstract import AbstractShield
from battle.equipment.shield.wood import Wood as Shield_Wood
from battle.equipment.shield.steel import Steel as Shield_Steel


class UnitTest_Battle_ShieldTest(UnitTest_Battle_Generic):
    def testArcheryShieldDefence(self):
        self.disableRandomChoice(True)

        unit = self.createUnit(
            shieldType=self.TYPE_SHIELD_WOOD,
            shieldDurability=100
        )

        self.assertTrue(AbstractShield().tryBlocking(50, unit))
        self.assertEqual(unit.shieldDurability, 50)
