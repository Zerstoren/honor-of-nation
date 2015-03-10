from tests.selenium.Equipment.generic import Selenium_Equipment_Generic
from tests.selenium.generic import Selenium_Generic
import tests.rerun

class Selenium_Equipment_UnitTest(Selenium_Generic):
    def setUp(self):
        super().setUp()
        # self.weapon = self.createEquipmentWeapon(self.user)
        # self.armor = self.createEquipmentArmor(self.user)

    @tests.rerun.retry()
    def testAddUnitBase(self):
        pass
        # self._openUnit()
        # self.getAddButton().click()
        #
        # self.selectArmor(self.armor)
        # self.selectWeapon(self.weapon)
        #
        # self.save()
        # self.operationIsSuccess()
        #
        # unitCollection = self.getUnitByUser(self.user)
        #
        # try:
        #     unitCollection[0]
        # except IndexError:
        #     self.fail('Unit is not saved')

    @tests.rerun.retry()
    def testAddUnitDifferenceFilter(self):
        pass
        # self._openUnit()
        #
        # self.getAddButton().click()
        # self.getFilterButton('solider').click()
        # self.selectArmor(self.armor)
        # self.selectWeapon(self.weapon)
        # self.save()
        # self.operationIsSuccess()
        # self.hideSuccessOperation()
        #
        # self.getAddButton().click()
        # self.getFilterButton('general').click()
        # self.selectArmor(self.armor)
        # self.selectWeapon(self.weapon)
        # self.save()
        # self.operationIsSuccess()
        # self.hideSuccessOperation()
        #
        # unitCollection = self.getUnitByUser(self.user)
        #
        # self.assertEqual(
        #     len(unitCollection.filter('type', 'solider')),
        #     1
        # )
        #
        # self.assertEqual(
        #     len(unitCollection.filter('type', 'general')),
        #     1
        # )

    @tests.rerun.retry()
    def testAddUnitCheckValues(self):
        pass
        # self._openUnit()
        # self.getAddButton().click()
        #
        # self.getFilterButton('general').click()
        #
        # self.setFieldValue('health', 100)
        # self.setFieldValue('agility', 100)
        # self.setFieldValue('absorption', 100)
        # self.setFieldValue('strength', 100)
        # self.setFieldValue('stamina', 100)
        # self.setFieldValue('troop_size', 100)
        #
        # self.selectArmor(self.armor)
        # self.selectWeapon(self.weapon)
        #
        # self.save()
        # self.operationIsSuccess()
        #
        # unitCollection = self.getUnitByUser(self.user)
        # unitDomain = unitCollection[0]
        #
        # self.assertEqual(unitDomain.getHealth(), 100)
        # self.assertEqual(unitDomain.getAgility(), 100)
        # self.assertEqual(unitDomain.getAbsorption(), 100)
        # self.assertEqual(unitDomain.getStrength(), 100)
        # self.assertEqual(unitDomain.getStamina(), 100)
        # self.assertEqual(unitDomain.getTroopSize(), 100)

    @tests.rerun.retry()
    def testLeftFilter(self):
        pass
        # self.unitSolider = self.createEquipmentUnit(self.user, uType='solider')
        # self.unitGeneral = self.createEquipmentUnit(self.user, uType='general')
        #
        # self._openUnit()
        #
        # self.setListFilterType('solider')
        # leather = self.getEquipmentByIdFromList(self.unitSolider)
        # self.assertStringContains(
        #     leather.byCss('.name').text,
        #     'solider'
        # )
        #
        # self.setListFilterType('general')
        # leather = self.getEquipmentByIdFromList(self.unitGeneral)
        # self.assertStringContains(
        #     leather.byCss('.name').text,
        #     'general'
        # )

    @tests.rerun.retry()
    def testRemoveUnit(self):
        pass
        # self.unit = self.createEquipmentUnit(self.user)
        #
        # self._openUnit()
        #
        # self.getEquipmentRemoveButton(self.unit).click()
        # self.operationIsSuccess()
        #
        # unitCollection = self.getUnitByUser(self.user)
        # self.assertEqual(
        #     len(unitCollection),
        #     0
        # )
