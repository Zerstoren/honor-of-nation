from tests.selenium.Equipment.generic import Selenium_Equipment_Generic
from tests.package.db.equipment import Equipment
from tests.package.dom import Dom
import tests.rerun

class Selenium_Equipment_ArmorTest(
    Selenium_Equipment_Generic,
    Equipment,
    Dom
):
    @tests.rerun.retry()
    def testAddArmorBase(self):
        self._openArmor()
        self.getAddButton().click()

        self.save()
        self.operationIsSuccess()

        armorCollection = self.getArmorByUser(self.user)

        try:
            armorDomain = armorCollection[0]
        except IndexError:
            self.fail('Armor is not saved')

    @tests.rerun.retry()
    def testAddArmorDifferenceFilter(self):
        self._openArmor()

        self.getAddButton().click()
        self.getFilterButton('leather').click()
        self.save()
        self.operationIsSuccess()
        self.hideSuccessOperation()

        self.getAddButton().click()
        self.getFilterButton('mail').click()
        self.save()
        self.operationIsSuccess()
        self.hideSuccessOperation()

        self.getAddButton().click()
        self.getFilterButton('plate').click()
        self.save()
        self.operationIsSuccess()
        self.hideSuccessOperation()

        armorCollection = self.getArmorByUser(self.user)

        self.assertEqual(
            len(armorCollection.filter('type', 'leather')),
            1
        )

        self.assertEqual(
            len(armorCollection.filter('type', 'mail')),
            1
        )

        self.assertEqual(
            len(armorCollection.filter('type', 'plate')),
            1
        )

    @tests.rerun.retry()
    def testAddArmorCheckValues(self):
        self._openArmor()
        self.getAddButton().click()

        self.setFieldValue('health', 100)
        self.setFieldValue('agility', 100)
        self.setFieldValue('absorption', 100)

        self.selectOptionValue(
            self.getField('shield'),
            'steel'
        )
        self.setFieldValue('shield_durability', 5000)
        self.setFieldValue('shield_blocking', 50)

        self.save()
        self.operationIsSuccess()

        armorCollection = self.getArmorByUser(self.user)
        armorDomain = armorCollection[0]

        self.assertEqual(armorDomain.getHealth(), 100)
        self.assertEqual(armorDomain.getAgility(), 100)
        self.assertEqual(armorDomain.getAbsorption(), 100)

        self.assertEqual(armorDomain.getShield(), True)
        self.assertEqual(armorDomain.getShieldBlocking(), 50)
        self.assertEqual(armorDomain.getShieldDurability(), 5000)

    @tests.rerun.retry()
    def testLeftFilter(self):
        self.armorLeather = self.addArmor(self.user, aType='leather')
        self.armorMail = self.addArmor(self.user, aType='mail')
        self.armorPlate = self.addArmor(self.user, aType='plate')

        self._openArmor()

        self.setListFilterType('leather')
        leather = self.getEquipmentByIdFromList(self.armorLeather)
        self.assertStringContains(
            leather.byCss('.name').text,
            'leather'
        )

        self.setListFilterType('mail')
        leather = self.getEquipmentByIdFromList(self.armorMail)
        self.assertStringContains(
            leather.byCss('.name').text,
            'mail'
        )

        self.setListFilterType('plate')
        leather = self.getEquipmentByIdFromList(self.armorPlate)
        self.assertStringContains(
            leather.byCss('.name').text,
            'plate'
        )

    def testRemoveArmor(self):
        self.armor = self.addArmor(self.user)

        self._openArmor()

        self.getEquipmentRemoveButton(self.armor).click()
        self.operationIsSuccess()

        armorCollection = self.getArmorByUser(self.user)
        self.assertEqual(
            len(armorCollection),
            0
        )
