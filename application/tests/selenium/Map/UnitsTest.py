from tests.selenium.Map.generic import Selenium_Map_Generic

from tests.package.db.town import Town
from tests.package.db.army import Army
from tests.package.db.equipment import Equipment
from tests.package.map import Map

import tests.rerun

from helpers.MapRegion import MapRegion


class Selenium_Map_UnitsTest(
    Selenium_Map_Generic,
    Town,
    Army,
    Equipment,
    Map
):
    def setUp(self):
        super().setUp()
        self.user = self.fixture.getUser(0)
        self.user.getMapper().save(self.user)
        self.region = self.fillTerrain(0, 0, 1, 1, landType=1)
        self.fillTerrain(0, 0, 15, 15, landType=1)
        self.openRegion(self.user, self.region)
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

        self.general = self.createArmy(self.town, self.unit_general, 1)
        self.solider = self.createArmy(self.town, self.unit_solider, 50)
        self.setArmySoliderToGeneral(self.solider, self.general)
        self.setArmyLeaveTown(self.general)

        self.login()

    def _waitForUnitsMoveComplete(self, general):
        general.extract(True)
        while True:
            self.waitForElement('.unit_move_path')
            self.waitForElementHide('.unit_move_path.c')

            general.extract(True)
            if len(general.getMovePath()) == 0:
                break

    @tests.rerun.retry()
    def testBaseMove(self):
        armyContainer = self.mapCell(0, 0).getContainer(self.general.getId())
        targetPosition = self.mapCell(4, 0).getItem()
        self.dragNDrop(armyContainer, targetPosition)

        self.waitForElement('.unit_move_path')

        self.general.extract(True)
        path = self.general.getMovePath()
        self.assertEquals(len(path), 4)
        self.assertEqual(path[0]['pos_id'], 1)
        self.assertEqual(path[1]['pos_id'], 2)
        self.assertEqual(path[2]['pos_id'], 3)
        self.assertEqual(path[3]['pos_id'], 4)

    @tests.rerun.retry()
    def testMoveMode4(self):
        armyContainer = self.mapCell(0, 0).getContainer(self.general.getId())
        targetPosition = self.mapCell(4, 0).getItem()

        armyContainer.click()
        self.byCssSelector('button.mode[data-mode="4"]').click()

        self.dragNDrop(armyContainer, targetPosition)

        self._waitForUnitsMoveComplete(self.general)

        self.general.extract(True)
        self.assertEqual(self.general.getLocation(), 4)

        collection = MapRegion(fromX=0, toX=6, fromY=0, toY=2).getCollection()
        mapUserCollectionVisible = collection.getMapVisible(self.user)

        self.assertEqual(len(mapUserCollectionVisible), 21)
