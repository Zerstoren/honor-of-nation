from tests.selenium.Map.generic import Selenium_Map_Generic

from tests.package.db.town import Town
from tests.package.db.army import Army
from tests.package.db.equipment import Equipment


class Selenium_Map_UnitsTest(
    Selenium_Map_Generic,
    Town,
    Army,
    Equipment
):
    def setUp(self):
        super().setUp()
        self.user = self.fixture.getUser(0)
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

    def testBaseShow(self):
        pass

