from tests.selenium.Equipment.generic import Selenium_Equipment_Generic
import tests.rerun

class Selenium_Equipment_UnitTest(Selenium_Equipment_Generic):
    def setUp(self):
        super().setUp()
        self.weapon = self.createEquipmentWeapon(self.user)
        self.armor = self.createEquipmentArmor(self.user)

    @tests.rerun.retry()
    def testAddUnitBase(self):
        self._openUnit()
        self.getAddButton().click()

        self.selectArmor(self.armor)
        self.selectWeapon(self.weapon)

        self.save()
        self.operationIsSuccess()

        unitCollection = self.getUnitByUser(self.user)

        try:
            unitCollection[0]
        except IndexError:
            self.fail('Unit is not saved')

    @tests.rerun.retry()
    def testAddUnitDifferenceFilter(self):
        self._openUnit()

        self.getAddButton().click()
        self.getFilterButton('solider').click()
        self.selectArmor(self.armor)
        self.selectWeapon(self.weapon)
        self.save()
        self.operationIsSuccess()
        self.hideSuccessOperation()

        self.getAddButton().click()
        self.getFilterButton('general').click()
        self.selectArmor(self.armor)
        self.selectWeapon(self.weapon)
        self.save()
        self.operationIsSuccess()
        self.hideSuccessOperation()


        unitCollection = self.getUnitByUser(self.user)

        self.assertEqual(
            len(unitCollection.filter('type', 'solider')),
            1
        )

        self.assertEqual(
            len(unitCollection.filter('type', 'general')),
            1
        )

    @tests.rerun.retry()
    def testAddUnitCheckValues(self):
        self._openUnit()
        self.getAddButton().click()

        self.setFieldValue('damage', 100)
        self.setFieldValue('speed', 100)
        self.setFieldValue('critical_damage', 3)
        self.setFieldValue('critical_chance', 10)

        self.save()
        self.operationIsSuccess()

        unitCollection = self.getUnitByUser(self.user)
        unitDomain = unitCollection[0]

        self.assertEqual(unitDomain.getDamage(), 100)
        self.assertEqual(unitDomain.getSpeed(), 100)
        self.assertEqual(unitDomain.getCriticalDamage(), 3.0)
        self.assertEqual(unitDomain.getCriticalChance(), 10)

    @tests.rerun.retry()
    def testLeftFilter(self):
        self.unitSword = self.createEquipmentUnit(self.user,wType='sword')
        self.unitBlunt = self.createEquipmentUnit(self.user, wType='blunt')
        self.unitSpear = self.createEquipmentUnit(self.user, wType='spear')
        self.unitBow = self.createEquipmentUnit(self.user, wType='bow')

        self._openUnit()

        self.setListFilterType('sword')
        leather = self.getEquipmentByIdFromList(self.unitSword)
        self.assertStringContains(
            leather.byCss('.name').text,
            'sword'
        )

        self.setListFilterType('blunt')
        leather = self.getEquipmentByIdFromList(self.unitBlunt)
        self.assertStringContains(
            leather.byCss('.name').text,
            'blunt'
        )

        self.setListFilterType('spear')
        leather = self.getEquipmentByIdFromList(self.unitSpear)
        self.assertStringContains(
            leather.byCss('.name').text,
            'spear'
        )

        self.setListFilterType('bow')
        leather = self.getEquipmentByIdFromList(self.unitBow)
        self.assertStringContains(
            leather.byCss('.name').text,
            'bow'
        )

    @tests.rerun.retry()
    def testRemoveUnit(self):
        self.unit = self.createEquipmentUnit(self.user)

        self._openUnit()

        self.getEquipmentRemoveButton(self.unit).click()
        self.operationIsSuccess()

        unitCollection = self.getUnitByUser(self.user)
        self.assertEqual(
            len(unitCollection),
            0
        )
