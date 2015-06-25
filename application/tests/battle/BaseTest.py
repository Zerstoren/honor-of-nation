from tests.battle.generic import Battle_Generic


class Battle_BaseTest(Battle_Generic):
    def setUp(self):
        super().setUp()
        self.attackerEquipmentUnit = self.createEquipmentUnit(self.attackerUser)
        self.attackerEquipmentGeneral = self.createEquipmentUnit(self.attackerUser, uType='general', troopSize=1000)

        self.defenderEquipmentUnit = self.createEquipmentUnit(self.defenderUser)
        self.defenderEquipmentGeneral = self.createEquipmentUnit(self.defenderUser, uType='general', troopSize=1000)

    def testSimpleBattle(self):
        unitsAttacker = self.createArmy(self.townAttacker, self.attackerEquipmentUnit, count=500)
        generalAttacker = self.createArmy(self.townAttacker, self.attackerEquipmentGeneral, count=1)
        self.setArmySoliderToGeneral(unitsAttacker, generalAttacker)

        unitsDefender = self.createArmy(self.townDefender, self.defenderEquipmentUnit, count=500)
        generalDefender = self.createArmy(self.townDefender, self.defenderEquipmentGeneral, count=1)
        self.setArmySoliderToGeneral(unitsDefender, generalDefender)

        self.prepare([generalAttacker], [generalDefender])
