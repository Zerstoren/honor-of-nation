from tests.selenium.generic import Selenium_Generic

from tests.package.interface import Interface
from tests.package.asserts import Asserts
from tests.package.db.town import Town

class Selenium_Equipment_Generic(
    Selenium_Generic,
    Asserts,
    Town,
    Interface
):
    def setUp(self):
        super().setUp()

        self.user = self.fixture.getUser(0)
        self.fillTerrain(0, 0, 1, 1)
        self.town = self.addTown(1, 1, self.user)

    def _openArmor(self):
        self.login(self.user)
        self.openTown(self.town)
        self.byCssSelector('.develop_armor').click()

    def _openWeapon(self):
        self.login(self.user)
        self.openTown(self.town)
        self.byCssSelector('.develop_weapon').click()

    def _openUnit(self):
        self.login(self.user)
        self.openTown(self.town)
        self.byCssSelector('.develop_unit').click()

    def getAddButton(self):
        return self.byCssSelector('.select-filter-equipment .add')

    def getField(self, name):
        return self.byCssSelector('.dev-wrapper .develop .field_%s' % name)

    def setFieldValue(self, name, value):
        field = self.getField(name)
        field.clear()
        field.send_keys(value)

    def getFilterButton(self, name):
        return self.byCssSelector('.select-equipment-type .%s' % name)

    def save(self):
        self.byCssSelector('.develop .save').click()

    def setListFilterType(self, fType):
        self.byCssSelector('.select-filter-equipment .filter.%s' % fType).click()

    def getEquipmentByIdFromList(self, equipment):
        return self.byCssSelector('.equipments-items div[data-id="%s"]' % str(equipment.getId()))

    def getEquipmentRemoveButton(self, equipment):
        return self.getEquipmentByIdFromList(equipment).byCss('button')