from tests.selenium.Town import generic

from tests.package.asserts import Asserts
from tests.package.interface import Interface
from tests.package.db.town import Town
from tests.package.db.army import Army
from tests.package.db.equipment import Equipment

import tests.rerun


class Selenium_Town_ArmyTest(
    generic.Selenium_Town_Generic,
    Asserts,
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
        self.unit = self.createEquipmentUnit(
            self.user,
            health=0,
            agility=0,
            absorption=0,
            stamina=0,
            strength=0,
            armor=self.armor,
            weapon=self.weapon
        )

        self.resources = self.user.getResources()
        self.resources.setRubins(1000000)
        self.resources.setWood(1000000)
        self.resources.setStone(1000000)
        self.resources.setSteel(1000000)
        self.resources.setEat(1000000)
        self.resources.getMapper().save(self.resources)

        self.login()
        self.openTown(self.town)

    @tests.rerun.retry()
    def testCreateArmy(self):
        self._createUnit(self.unit, 1)
        self.sleep(2)

        result = self.byCssSelectorMany('.unitsWrap ul li')
        self.assertEqual(
            len(result),
            1
        )