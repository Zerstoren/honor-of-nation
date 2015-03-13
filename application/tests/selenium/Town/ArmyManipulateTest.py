from tests.selenium.Town import generic

import tests.rerun

from tests.package.interface import Interface
from tests.package.db.town import Town
from tests.package.db.army import Army
from tests.package.db.equipment import Equipment

from service.Army import Service_Army

class Selenium_Town_ArmyManipulateTest(
    generic.Selenium_Town_Generic,
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

    def _combinateArmy(self):
        self.setArmySoliderToGeneral(self.solider_1, self.general_1)
        self.setArmySuiteToGeneral(self.solider_2, self.general_1)

        self.setArmySoliderToGeneral(self.solider_3, self.general_2)
        self.setArmySuiteToGeneral(self.solider_4, self.general_2)

        self.setArmySoliderToGeneral(self.solider_5, self.general_3)
        self.setArmySuiteToGeneral(self.solider_6, self.general_3)

        self.setArmySoliderToGeneral(self.solider_7, self.general_4)
        self.setArmySuiteToGeneral(self.solider_8, self.general_4)

        self.setArmySoliderToGeneral(self.general_2, self.general_1)
        self.setArmySoliderToGeneral(self.general_3, self.general_1)
        self.setArmySoliderToGeneral(self.general_4, self.general_1)

    @tests.rerun.retry()
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

    @tests.rerun.retry()
    def testSplitUnits(self):
        self._selectArmyInList(self.solider_1)
        self._armyAction('split')

        self.selectRange(
            self.byCssSelector('.split-block input[type="range"]'),
            25
        )
        self.byCssSelector('.confirm-split').click()
        self.waitForSocket()

        self.solider_1.extract(True)
        result = Service_Army().load(self.user, self.town.getMap().getPosition(), {'inBuild': True})
        self.assertEqual(len(result), 13)
        self.assertEqual(self.solider_1.getCount(), 25)


    @tests.rerun.retry()
    def testLeaveTown(self):
        self._selectArmyInList(self.general_1)
        self._armyAction('move_out')
        self.waitForSocket()

        self.general_1.extract(True)
        self.assertFalse(self.general_1.getInBuild())

        self._selectArmyInList(self.solider_1)
        self._isArmyActionDisabled('move_out')

    @tests.rerun.retry()
    def testAddSoliderToGeneral(self):
        self._selectArmyInList(self.general_1)
        self._selectArmyInList(self.solider_1)
        self._selectArmyInList(self.solider_2)
        self._armyAction('add_soliders_to_general')

        self.waitForSocket()

        unitDetail = Service_Army().loadDetail(self.user, self.general_1.getId())
        self.assertEqual(len(unitDetail['sub_army']), 2)

    @tests.rerun.retry()
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

    @tests.rerun.retry()
    def testRemoveUnit(self):
        self._selectArmyInList(self.general_1)
        self._armyAction('dissolution')
        self.byCssSelector('.confirm-dissolution').click()

        self.waitForSocket()

        self._armyNotInList(self.general_1)

    @tests.rerun.retry()
    def testMergeGenerals(self):
        self.dragNDrop(
            self._getArmyInList(self.general_2),
            self._getArmyInList(self.general_1)
        )
        self.waitForSocket()
        self._armyNotInList(self.general_2)

        unitDetail = Service_Army().loadDetail(self.user, self.general_1.getId())
        self.assertEqual(len(unitDetail['sub_army']), 1)
        self.assertEqual(unitDetail['sub_army'][0]['current'].getId(), self.general_2.getId())

    @tests.rerun.retry()
    def testDetailLoadIsSuccess(self):
        self._combinateArmy()
        self._openCommanderDetail(self.general_1)

        self._armyNotShowInDetail(self.solider_3)

        self._getArmyInDetail(self.general_2).click()
        self._getArmyInDetail(self.solider_3)
        self._getArmyInDetail(self.solider_4)

        self._getArmyInDetail(self.general_3).click()
        self._getArmyInDetail(self.solider_5)
        self._getArmyInDetail(self.solider_6)

        self._getArmyInDetail(self.general_4).click()
        self._getArmyInDetail(self.solider_7)
        self._getArmyInDetail(self.solider_8)

    @tests.rerun.retry()
    def testMoveSuiteToBufferAndBack(self):
        self._combinateArmy()
        self._openCommanderDetail(self.general_1)

        self.assertEqual(self.general_1.getSuite().getId(), self.solider_2.getId())

        self.dragNDrop(
            self._getArmyInDetail(self.solider_2),
            self._getBuffer()
        )
        self.waitForSocket()
        self.general_1.extract(True)
        self.assertEqual(self.general_1.getSuite(), None)
        self._getArmyInDetail(self.solider_2, self._getBuffer())

        self.dragNDrop(
            self._getArmyInDetail(self.solider_2),
            self._getMiddleSuite()
        )
        self.waitForSocket()
        self.general_1.extract(True)
        self.assertEqual(self.general_1.getSuite().getId(), self.solider_2.getId())

    @tests.rerun.retry()
    def testMoveBottomSuiteToBufferAndBack(self):
        self._combinateArmy()
        self._openCommanderDetail(self.general_1)
        self._getArmyInDetail(self.general_2).click()

        self.assertEqual(self.general_2.getSuite().getId(), self.solider_4.getId())

        self.dragNDrop(
            self._getArmyInDetail(self.solider_4),
            self._getBuffer()
        )
        self.waitForSocket()
        self.general_2.extract(True)
        self.assertEqual(self.general_2.getSuite(), None)
        self._getArmyInDetail(self.solider_4, self._getBuffer())

        self.dragNDrop(
            self._getArmyInDetail(self.solider_4),
            self._getBottomSuite()
        )
        self.waitForSocket()
        self.general_2.extract(True)
        self.assertEqual(self.general_2.getSuite().getId(), self.solider_4.getId())

    @tests.rerun.retry()
    def testMoveMiddleUnitsListToBufferAndBack(self):
        self._combinateArmy()
        self._openCommanderDetail(self.general_1)

        self.assertEqual(self.general_2.getCommander().getId(), self.general_1.getId())

        self.dragNDrop(
            self._getArmyInDetail(self.general_2),
            self._getBuffer()
        )
        self.waitForSocket()
        self.general_2.extract(True)
        self.assertEqual(self.general_2.getCommander(), None)
        self._getArmyInDetail(self.general_2, self._getBuffer())

        self.dragNDrop(
            self._getArmyInDetail(self.general_2),
            self._getMiddleUnitsList()
        )
        self.waitForSocket()
        self.general_2.extract(True)
        self.assertEqual(self.general_2.getCommander().getId(), self.general_1.getId())

    @tests.rerun.retry()
    def testMoveBottomUnitListToBufferAndBack(self):
        self._combinateArmy()
        self._openCommanderDetail(self.general_1)
        self._getArmyInDetail(self.general_2).click()

        self.assertEqual(self.solider_3.getCommander().getId(), self.general_2.getId())

        self.dragNDrop(
            self._getArmyInDetail(self.solider_3),
            self._getBuffer()
        )
        self.waitForSocket()
        self.solider_3.extract(True)
        self.assertEqual(self.solider_3.getCommander(), None)
        self._getArmyInDetail(self.solider_3, self._getBuffer())

        self.dragNDrop(
            self._getArmyInDetail(self.solider_3),
            self._getBottomUnitsList()
        )
        self.waitForSocket()
        self.solider_3.extract(True)
        self.assertEqual(self.solider_3.getCommander().getId(), self.general_2.getId())
        self._getArmyInDetail(self.solider_3, self._getBottomUnitsList())
