from tests.selenium.Main.Menu.Admin import generic


class Selenium_Main_Menu_Admin_UserTest(generic.Selenium_Main_Menu_Admin_Generic):
    def _selectUserForEdit(self, user):
        select = self.byXPath('//select[@ng-model="popup.admin.vars.usersSelectedToEdit"]')
        self.selectOptionText(select, user.getLogin())

    def testSetResources(self):
        user = self.fixture.getUser(0)
        userForTest = self.fixture.getUser(1)

        self.login()

        self.createWindow(userForTest.getLogin())
        self.useWindow(userForTest.getLogin())
        self.login(userForTest)

        self.useWindow('main')

        self._getMenuItem('admin').click()
        self._selectTestAdminBlock('users')

        self._selectUserForEdit(userForTest)
        self.waitForSocket()

        resourcesToSet = {
            'rubins': 150000,
            'wood': 150000,
            'steel': 1500,
            'stone': 1500,
            'eat': 150000,
            'gold': 15000000,
        }

        self.waitForSocket()
        for resource in resourcesToSet:
            self.byNg('popup.admin.vars.userSelectEdit.resources.' + resource).\
                send_keys(self.keys.BACK_SPACE + str(resourcesToSet[resource]))

        self.byXPath('//button[@ng-click="popup.admin.func.userSaveResource()"]').click()
        self.waitForSocket()

        self.useWindow(userForTest.getLogin())
        self.waitForSocket()

        resources = self._getResources()

        self.assertEqual(resources, resourcesToSet)

    def testMap(self):
        self._fillMap(253)

        user = self.fixture.getUser(0)
        self.login(user)

        targetUser = self.fixture.getUser(1)
        self.createWindow(targetUser.getLogin())
        self.useWindow(targetUser.getLogin())
        self.login(targetUser)
        self._setCameraMapPosition(40, 40)

        self.useWindow('main')

        self._getMenuItem('admin').click()
        self._selectTestAdminBlock('users')

        self.waitForSocket()
        self._selectUserForEdit(targetUser)

        self.byNg('popup.admin.vars.userFromPosX').send_keys('38')
        self.byNg('popup.admin.vars.userFromPosY').send_keys('38')
        self.byNg('popup.admin.vars.userToPosX').send_keys('42')
        self.byNg('popup.admin.vars.userToPosY').send_keys('42')

        self.byNg('popup.admin.func.userShowHiddenMap()', 'ng-click').click()
        self.waitForSocket()

        self.useWindow(targetUser.getLogin())
        self.waitForSocket()

        self.assertFalse(
            self._getMap(40, 40).isHidden()
        )
