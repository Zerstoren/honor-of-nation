from tests.selenium.Main.Menu.Admin import generic
import models.Resources.Factory


class Selenium_Main_Menu_Admin_ResourceTest(generic.Selenium_Main_Menu_Admin_Generic):
    def setUp(self):
        super().setUp()
        self.map = self._fillMapOneItem(40, 40)

    def _open(self):
        self.login()
        self._getMenuItem('admin').click()
        self._selectTestAdminBlock('resource')

    def testCreateResource_WithoutTown(self):
        self._open()
        self._resourceCreateButton().click()

        self.byNg('popup.admin.vars.resourceData.position').send_keys('40x40')
        self.byNg('popup.admin.vars.resourceData.amount').send_keys('25000000')
        self.byNg('popup.admin.vars.resourceData.output').send_keys('25000')
        self.byNg('popup.admin.vars.resourceData.base_output').send_keys('25000')
        self.selectOptionText(self.byNg('popup.admin.vars.resourceData.type'), 'камень')

        self.byNg('popup.admin.func.resourceSave()', 'ng-click').click()
        self.waitForSocket()

        resourceDomain = models.Resources.Factory.factory.getByMap(self.map)

        self.assertEqual(resourceDomain.getPosition(), self.map)
        self.assertEqual(resourceDomain.getOutput(), 25000)
        self.assertEqual(resourceDomain.getBaseOutput(), 25000)
        self.assertEqual(resourceDomain.getAmount(), 25000000)
        self.assertEqual(resourceDomain.getType(), resourceDomain.TYPE_STONE)
        self.assertEqual(resourceDomain.getUser(), None)
        self.assertEqual(resourceDomain.getTown(), None)

    def testCreateResource_WithTown(self):
        self._open()
        user = self.fixture.getUser(0)
        town = self._createTown(
            self._fillMapOneItem(38, 38),
            user
        )
        self.map.addAccessToUser(user)

        self._resourceCreateButton().click()

        self.byNg('popup.admin.vars.resourceData.position').send_keys('%sx%s' %
            (self.map.getPositionX(), self.map.getPositionY()))

        self.byNg('popup.admin.vars.resourceData.amount').send_keys('25000000')
        self.byNg('popup.admin.vars.resourceData.output').send_keys('25000')
        self.byNg('popup.admin.vars.resourceData.base_output').send_keys('25000')
        self.selectOptionText(self.byNg('popup.admin.vars.resourceData.type'), 'камень')
        self.selectOptionText(self.byNg('popup.admin.vars.resourceData.user'), user.getLogin())
        self.waitForSocket()

        self.selectOptionText(self.byNg('popup.admin.vars.resourceData.town'), town.getName())

        self.byNg('popup.admin.func.resourceSave()', 'ng-click').click()
        self.waitForSocket()

        #self.sleep(50)

        resourceDomain = models.Resources.Factory.factory.getByMap(self.map)

        self.assertEqual(resourceDomain.getPosition(), self.map)
        self.assertEqual(resourceDomain.getOutput(), 25000)
        self.assertEqual(resourceDomain.getBaseOutput(), 25000)
        self.assertEqual(resourceDomain.getAmount(), 25000000)
        self.assertEqual(resourceDomain.getType(), resourceDomain.TYPE_STONE)
        self.assertEqual(resourceDomain.getTown(), town)
        self.assertEqual(resourceDomain.getUser(), user)

    def testEditResource(self):
        user = self.fixture.getUser(0)
        town = self._createTown(
            self._fillMapOneItem(38, 38),
            user
        )
        self.map.addAccessToUser(user)

        resource = self._createResource(self.map, user, town)

        newUser = self.fixture.getUser(1)
        newTown = self._createTown(self._fillMapOneItem(38, 39), newUser)
        self.map.addAccessToUser(newUser)

        self._open()

        self.byNg('popup.admin.vars.resourceSearchValue').send_keys('%sx%s' % (
            self.map.getPositionX(),
            self.map.getPositionY()
        ))
        self.byNg('popup.admin.func.resourceSearch()', by='ng-click').click()
        self.waitForSocket()

        tmp = self.byNg('popup.admin.vars.resourceData.amount')
        tmp.clear()
        tmp.send_keys('3000')

        tmp = self.byNg('popup.admin.vars.resourceData.output')
        tmp.clear()
        tmp.send_keys('1000')

        self.selectOptionText(self.byNg('popup.admin.vars.resourceData.user'), newUser.getLogin())
        self.waitForSocket()
        self.selectOptionText(self.byNg('popup.admin.vars.resourceData.town'), newTown.getName())
        self.byNg('popup.admin.func.resourceSave()', 'ng-click').click()

        self.fullCleanCache()

        resourceDomain = models.Resources.Factory.factory.getByMap(self.map)

        self.assertEqual(resourceDomain.getOutput(), 1000)
        self.assertEqual(resourceDomain.getAmount(), 3000)
        self.assertEqual(resourceDomain.getTown().getId(), newTown.getId())
        self.assertEqual(resourceDomain.getUser().getId(), newUser.getId())