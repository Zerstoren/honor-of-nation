from tests.selenium.Town import generic

from tests.package.interface import Interface
from tests.package.dom import Dom
from tests.package.db.town import Town
from tests.package.db.army import Army
from tests.package.db.equipment import Equipment

from service.Army import Service_Army

class Selenium_Town_ArmyManipulate(
    generic.Selenium_Town_Generic,
    Dom,
    Town,
    Army,
    Equipment,
    Interface
):
    def setUp(self):
        super().setUp()
        self.terrain = self.fillTerrain(0, 0, 1, 1)

        self.user = self.fixture.getUser(0)

        self.town = self.addTown(0, 0, self.user, 1)

        self.armor = self.createEquipmentArmor(self.user, health=0, agility=0, absorption=0)
        self.weapon = self.createEquipmentWeapon(self.user, damage=0, speed=0, critical_chance=0, critical_damage=0)
        self.unit_general = self.createEquipmentUnit(
            self.user,
            uType='general',
            troopSize=1000,
            health=0,
            agility=0,
            absorption=0,
            stamina=0,
            strength=0,
            armor=self.armor,
            weapon=self.weapon,
        )

        self.unit_solider = self.createEquipmentUnit(
            self.user,
            health=0,
            agility=0,
            absorption=0,
            stamina=0,
            strength=0,
            armor=self.armor,
            weapon=self.weapon
        )

        self.general_1 = self.createArmy(self.town, self.unit_general, 1)
        self.general_2 = self.createArmy(self.town, self.unit_general, 1)
        self.general_3 = self.createArmy(self.town, self.unit_general, 1)
        self.general_4 = self.createArmy(self.town, self.unit_general, 1)

        self.solider_1 = self.createArmy(self.town, self.unit_solider, 50)
        self.solider_2 = self.createArmy(self.town, self.unit_solider, 50)
        self.solider_3 = self.createArmy(self.town, self.unit_solider, 50)
        self.solider_4 = self.createArmy(self.town, self.unit_solider, 50)
        self.solider_5 = self.createArmy(self.town, self.unit_solider, 50)
        self.solider_6 = self.createArmy(self.town, self.unit_solider, 50)
        self.solider_7 = self.createArmy(self.town, self.unit_solider, 50)
        self.solider_8 = self.createArmy(self.town, self.unit_solider, 50)

        self.login()
        self.openTown(self.town)
        self.waitForElement('.listUnits .units li')

    def testMergeUnits(self):
        self._selectArmyInList(self.solider_1)
        self._selectArmyInList(self.solider_2)
        self._armyAction('merge')

        self.waitForSocket()

        self.solider_1.extract(True)
        self.assertEqual(
            self.solider_1.getCount(),
            100
        )

        self._selectArmyInList(self.solider_1)
        self._selectArmyInList(self.general_1)
        self._isArmyActionDisabled('merge')

    # def testSplitUnits(self):
    #     self._selectArmyInList(self.solider_1)
    #     self._armyAction('split')
    #     self.byCssSelector('.confirm-split').click()
    #
    #     self.sleep(15)

    def testLeaveTown(self):
        self._selectArmyInList(self.general_1)
        self._armyAction('move_out')
        self.waitForSocket()

        self.general_1.extract(True)
        self.assertFalse(self.general_1.getInBuild())

        self._selectArmyInList(self.solider_1)
        self._isArmyActionDisabled('move_out')


    def testAddSoliderToGeneral(self):
        self._selectArmyInList(self.general_1)
        self._selectArmyInList(self.solider_1)
        self._selectArmyInList(self.solider_2)
        self._armyAction('add_soliders_to_general')

        self.waitForSocket()

        unitDetail = Service_Army().loadDetail(self.user, self.general_1.getId())
        self.assertEqual(len(unitDetail['sub_army']), 2)

    def testAddSuiteToGeneral(self):
        self._selectArmyInList(self.general_1)
        self._selectArmyInList(self.solider_1)
        self._armyAction('add_suite')

        self.waitForSocket()

        self.general_1.extract(True)
        self.assertEqual(
            self.general_1.getSuite().getId(),
            self.solider_1.getId()
        )

    # def testRemoveUnit(self):
    #     self._selectArmyInList(self.general_1)
    #     self._armyAction('dissolution')
    #     self.byCssSelector('.confirm-dissolution').click()
    #
    #     self.waitForSocket()
    #
    #     self._armyNotInList(self.general_1)
    #