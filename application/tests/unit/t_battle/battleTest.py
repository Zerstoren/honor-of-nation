from tests.unit.t_battle.generic import UnitTest_Battle_Generic
from battle.places.field import Field as Location_Field

from battle.simulate.battle import Battle

class UnitTest_Battle_BattleTest(UnitTest_Battle_Generic):
    # def testArcheryOneFrontFight(self):
    #     attackerUnit = self.createUnit(
    #         weaponType=self.TYPE_WEAPON_BOW,
    #         damage=85,
    #         attackSpeed=9,
    #         criticalChance=1,
    #         criticalDamage=1.5,
    #         health=80,
    #         agility=10
    #     )
    #
    #     defenderUnit = self.createUnit(
    #         weaponType=self.TYPE_WEAPON_BOW,
    #         damage=85,
    #         attackSpeed=550,
    #         health=80,
    #         agility=10,
    #         criticalChance=1,
    #         criticalDamage=1.5
    #     )
    #
    #     attackerGroup = self.createGroup(100, attackerUnit)
    #     defenderGroup = self.createGroup(1, defenderUnit)
    #
    #     attackerFrontCollection = self.createFrontCollection(False)
    #     defenderFrontCollection = self.createFrontCollection(True)
    #
    #     attackerFrontCollection.get(self.FRONT_AVANGARD).addGroup(attackerGroup)
    #     defenderFrontCollection.get(self.FRONT_AVANGARD).addGroup(defenderGroup)
    #
    #     self.disableRandomChoice(True)
    #     self.disableRandomInt(False)
    #
    #     battle = Battle()
    #     battle.importData(
    #         attackerFrontCollection,
    #         defenderFrontCollection,
    #         Location_Field.getInstance()
    #     )
    #     battle.simulate()
    #
    # def testMeleeOneFrontFight(self):
    #     attackerUnit = self.createUnit(
    #         weaponType=self.TYPE_WEAPON_SWORD,
    #         damage=20,
    #         attackSpeed=10,
    #         criticalChance=1,
    #         criticalDamage=1,
    #         health=80,
    #         agility=10
    #     )
    #
    #     defenderUnit = self.createUnit(
    #         weaponType=self.TYPE_WEAPON_SWORD,
    #         damage=20,
    #         attackSpeed=10,
    #         criticalChance=100,
    #         criticalDamage=4,
    #         health=80,
    #         agility=10
    #     )
    #
    #     attackerGroup = self.createGroup(2, attackerUnit)
    #     defenderGroup = self.createGroup(1, defenderUnit)
    #
    #     attackerFrontCollection = self.createFrontCollection(False)
    #     defenderFrontCollection = self.createFrontCollection(True)
    #
    #     attackerFrontCollection.get(self.FRONT_AVANGARD).addGroup(attackerGroup)
    #     defenderFrontCollection.get(self.FRONT_AVANGARD).addGroup(defenderGroup)
    #
    #     self.disableRandomChoice(True)
    #     self.disableRandomInt(False)
    #
    #     battle = Battle()
    #     battle.importData(
    #         attackerFrontCollection,
    #         defenderFrontCollection,
    #         Location_Field.getInstance()
    #     )
    #     battle.simulate()

    def testMeleeFullFront(self):
        attackerUnit = self.createUnit(
            weaponType=self.TYPE_WEAPON_SWORD,
            damage=200,
            attackSpeed=1000,
            criticalChance=1,
            criticalDamage=1,
            health=80,
            agility=10
        )

        defenderUnit = self.createUnit(
            weaponType=self.TYPE_WEAPON_SWORD,
            damage=20,
            attackSpeed=10,
            criticalChance=1,
            criticalDamage=4,
            health=80,
            agility=10
        )

        attackerGroup = self.createGroup(50, attackerUnit)
        defenderGroupAvangard = self.createGroup(1, defenderUnit)
        defenderGroupLeftFront = self.createGroup(1, defenderUnit)
        defenderGroupRightFront = self.createGroup(1, defenderUnit)
        defenderGroupRear = self.createGroup(1, defenderUnit)

        attackerFrontCollection = self.createFrontCollection(False)
        defenderFrontCollection = self.createFrontCollection(True)

        attackerFrontCollection.get(self.FRONT_AVANGARD).addGroup(attackerGroup)

        defenderFrontCollection.get(self.FRONT_AVANGARD).addGroup(defenderGroupAvangard)
        defenderFrontCollection.get(self.FRONT_LEFT_FLANG).addGroup(defenderGroupLeftFront)
        defenderFrontCollection.get(self.FRONT_RIGHT_FLANG).addGroup(defenderGroupRightFront)
        defenderFrontCollection.get(self.FRONT_REAR).addGroup(defenderGroupRear)

        self.disableRandomChoice(True)
        self.disableRandomInt(False)

        battle = Battle()
        battle.importData(
            attackerFrontCollection,
            defenderFrontCollection,
            Location_Field.getInstance()
        )
        battle.simulate()