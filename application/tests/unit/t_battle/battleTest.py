from tests.unit.t_battle.generic import UnitTest_Battle_Generic
from battle.places.field import Field as Location_Field

from battle.simulate.battle import Battle

class UnitTest_Battle_BattleTest(UnitTest_Battle_Generic):
    def testArcheryOneFrontFight(self):
        attackerUnit = self.createUnit(
            weaponType=self.TYPE_WEAPON_BOW,
            damage=1,
            attackSpeed=100,
            health=10,
            agility=10
        )

        defenderUnit = self.createUnit(
            weaponType=self.TYPE_WEAPON_BOW,
            damage=1,
            attackSpeed=1,
            health=10,
            agility=10
        )

        attackerGroup = self.createGroup(100, attackerUnit)
        defenderGroup = self.createGroup(100, defenderUnit)

        attackerFrontCollection = self.createFrontCollection(False)
        defenderFrontCollection = self.createFrontCollection(True)

        attackerFrontCollection.get(self.FRONT_AVANGARD).addGroup(attackerGroup)
        defenderFrontCollection.get(self.FRONT_AVANGARD).addGroup(defenderGroup)

        self.disableRandomChoice(True)
        self.disableRandomInt(False)

        battle = Battle()
        battle.importData(
            attackerFrontCollection,
            defenderFrontCollection,
            Location_Field.getInstance()
        )
        battle.simulate()
