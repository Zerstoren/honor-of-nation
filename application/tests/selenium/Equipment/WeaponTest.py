from tests.selenium.Equipment.generic import Selenium_Equipment_Generic
import tests.rerun

class Selenium_Equipment_WeaponTest(Selenium_Equipment_Generic):
    @tests.rerun.retry()
    def testAddWeaponBase(self):
        self._openWeapon()
        self.getAddButton().click()

        self.save()
        self.operationIsSuccess()

        weaponCollection = self.getWeaponByUser(self.user)

        try:
            weaponCollection[0]
        except IndexError:
            self.fail('Weapon is not saved')

    @tests.rerun.retry()
    def testAddWeaponDifferenceFilter(self):
        self.showBrowserLogs = True
        self._openWeapon()

        self.getAddButton().click()
        self.sleep(1)
        self.getFilterButton('sword').click()
        self.save()
        self.operationIsSuccess()
        self.hideSuccessOperation()

        self.getAddButton().click()
        self.sleep(1)
        self.getFilterButton('blunt').click()
        self.save()
        self.operationIsSuccess()
        self.hideSuccessOperation()

        self.getAddButton().click()
        self.sleep(1)
        self.getFilterButton('spear').click()
        self.save()
        self.operationIsSuccess()
        self.hideSuccessOperation()

        self.getAddButton().click()
        self.sleep(1)
        self.getFilterButton('bow').click()
        self.save()
        self.operationIsSuccess()
        self.hideSuccessOperation()

        weaponCollection = self.getWeaponByUser(self.user)
        for i in weaponCollection:
            print(i.getType())

        self.assertEqual(
            len(weaponCollection.filter('type', 'sword')),
            1
        )

        self.assertEqual(
            len(weaponCollection.filter('type', 'blunt')),
            1
        )

        self.assertEqual(
            len(weaponCollection.filter('type', 'spear')),
            1
        )

        self.assertEqual(
            len(weaponCollection.filter('type', 'bow')),
            1
        )

    @tests.rerun.retry()
    def testAddWeaponCheckValues(self):
        self._openWeapon()
        self.getAddButton().click()

        self.setFieldValue('damage', 100)
        self.setFieldValue('speed', 100)
        self.setFieldValue('critical_damage', 3)
        self.setFieldValue('critical_chance', 10)

        self.save()
        self.operationIsSuccess()

        weaponCollection = self.getWeaponByUser(self.user)
        weaponDomain = weaponCollection[0]

        self.assertEqual(weaponDomain.getDamage(), 100)
        self.assertEqual(weaponDomain.getSpeed(), 100)
        self.assertEqual(weaponDomain.getCriticalDamage(), 3.0)
        self.assertEqual(weaponDomain.getCriticalChance(), 10)

    @tests.rerun.retry()
    def testLeftFilter(self):
        self.weaponSword = self.createEquipmentWeapon(self.user,wType='sword')
        self.weaponBlunt = self.createEquipmentWeapon(self.user, wType='blunt')
        self.weaponSpear = self.createEquipmentWeapon(self.user, wType='spear')
        self.weaponBow = self.createEquipmentWeapon(self.user, wType='bow')

        self._openWeapon()

        self.setListFilterType('sword')
        leather = self.getEquipmentByIdFromList(self.weaponSword)
        self.assertStringContains(
            leather.byCss('.name').text,
            'sword'
        )

        self.setListFilterType('blunt')
        leather = self.getEquipmentByIdFromList(self.weaponBlunt)
        self.assertStringContains(
            leather.byCss('.name').text,
            'blunt'
        )

        self.setListFilterType('spear')
        leather = self.getEquipmentByIdFromList(self.weaponSpear)
        self.assertStringContains(
            leather.byCss('.name').text,
            'spear'
        )

        self.setListFilterType('bow')
        leather = self.getEquipmentByIdFromList(self.weaponBow)
        self.assertStringContains(
            leather.byCss('.name').text,
            'bow'
        )

    @tests.rerun.retry()
    def testRemoveWeapon(self):
        self.weapon = self.createEquipmentWeapon(self.user)

        self._openWeapon()

        self.getEquipmentRemoveButton(self.weapon).click()
        self.operationIsSuccess()

        weaponCollection = self.getWeaponByUser(self.user)
        self.assertEqual(
            len(weaponCollection),
            0
        )
