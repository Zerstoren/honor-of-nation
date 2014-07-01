from tests.selenium.Town.Develop import generic
from models import ArmorBox


class Selenium_Town_Develop_ArmorDevelopTest(generic.Selenium_Town_Develop_Generic):
    def _setManyResources(self, userDomain):
        """
        :type userDomain: models.User.UserDomain.UserDomain
        """
        resources = userDomain.getSubDomainResource()
        resourcesEdit = resources.edit()
        resourcesEdit.setResource(resources.RESOURCE_EAT, 100000000)
        resourcesEdit.setResource(resources.RESOURCE_RUBINS, 100000000)
        resourcesEdit.setResource(resources.RESOURCE_WOOD, 100000000)
        resourcesEdit.setResource(resources.RESOURCE_STONE, 100000000)
        resourcesEdit.setResource(resources.RESOURCE_STEEL, 100000000)
        resourcesEdit.getMapper().save(resourcesEdit)

    def _loginToTownArmor(self, userDomain=None):
        self.login(userDomain)

        self.waitForSocket()
        self.moveToPath('townDevArmor', {
            'townId': str(self.town.getId())
        })

        self.waitForSocket()

    def testBaseCreate(self):
        health = 600
        absorption = 40
        agility = 40
        armorType = ArmorBox.ArmorBoxDomain.ArmorBoxDomain.ARMOR_MAIL

        shieldMaterial = ArmorBox.ArmorBoxDomain.ArmorBoxDomain.SHIELD_STEEL
        shieldDurability = 500
        shieldBlock = 70

        horseHealth = 500
        horseSlope = 80

        self._setManyResources(self.fixture.getUser(0))
        self._loginToTownArmor()

        self.selectOptionValue(
            self.byNg('vars.armor.armor_type'),
            armorType
        )

        self.byNg('vars.armor.health').clear()
        self.byNg('vars.armor.health').send_keys(health)

        self.byNg('vars.armor.absorption').clear()
        self.byNg('vars.armor.absorption').send_keys(absorption)

        self.byNg('vars.armor.agility').clear()
        self.byNg('vars.armor.agility').send_keys(agility)


        self.byNg('vars.armor.shield_use').click()
        self.selectOptionValue(
            self.byNg('vars.armor.shield_type'),
            shieldMaterial
        )

        self.byNg('vars.armor.shield_durability').clear()
        self.byNg('vars.armor.shield_durability').send_keys(shieldDurability)

        self.byNg('vars.armor.shield_block').clear()
        self.byNg('vars.armor.shield_block').send_keys(shieldBlock)


        self.byNg('vars.armor.horse_use').click()
        self.byNg('vars.armor.horse_health').clear()
        self.byNg('vars.armor.horse_health').send_keys(horseHealth)

        self.byNg('vars.armor.horse_slope').clear()
        self.byNg('vars.armor.horse_slope').send_keys(horseSlope)

        self.byNg('func.createArmor()', 'ng-click').click()
        self.waitForSocket()

        armorDomain = ArmorBox.Factory.factory.getByUser(self.fixture.getUser(0)).get(0)
        """:type: models.ArmorBox.ArmorBoxDomain.ArmorBoxDomain """

        self.assertEqual(armorDomain.getArmorType(), armorType)
        self.assertEqual(armorDomain.getHealth(), health)
        self.assertEqual(armorDomain.getAgility(), agility)
        self.assertEqual(armorDomain.getAbsorption(), absorption)

        self.assertEqual(armorDomain.getShieldType(), shieldMaterial)
        self.assertEqual(armorDomain.getShieldDurability(), shieldDurability)
        self.assertEqual(armorDomain.getShieldBlock(), shieldBlock)

        self.assertEqual(armorDomain.getHorseHealth(), horseHealth)
        self.assertEqual(armorDomain.getHorseSlope(), horseSlope)
        print(armorDomain.toObject())
