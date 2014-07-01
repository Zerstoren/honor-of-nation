from tests.selenium.Main.Interface import generic


class Selenium_Main_Interface_BottomInterfaceTest(generic.Selenium_Main_Interface_Generic):

    def testInfoAfterSelectResource(self):
        self._prepareResources()
        self.login()

        self._getMap(51, 51).getItem().click()
        interfaceBlock = self.byNg("menuInterface.type == 'resource'", 'ng-show');
        self.assertEqual(
            interfaceBlock.byCss('.type').text,
            'Рубиновый приск'
        )
        self.assertEqual(
            interfaceBlock.byCss('.holder > span').text,
            'отсутствует'
        )
        self.assertEqual(
            interfaceBlock.byCss('.amount > span').get_attribute('ng-hint'),
            '1 000 000'
        )
        self.assertEqual(
            interfaceBlock.byCss('.base_output > span').get_attribute('ng-hint'),
            '15 000'
        )

    def testInfoAfterSelectTown(self):
        self._prepareTown()
        self.login()

        self._getMap(50, 50).getItem().click()

        interfaceBlock = self.byNg("menuInterface.type == 'towns'", 'ng-show')
        self.assertEqual(
            interfaceBlock.byCss('.type').text,
            'Село - ' + self.town1.getName()
        )
        self.assertEqual(
            interfaceBlock.byCss('.holder > a').text,
            self.user.getLogin()
        )

        self.assertEqual(
            interfaceBlock.byCss('.population').text,
            'Население: 5 000'
        )

    def testBlockChangeCoordinate_AfterClickObject(self):
        self._prepareTown()
        self.login()

        self._moveCursor(self._getMap(48, 48))
        self.assertEqual(
            self.byCssSelector('.menu_interface .left .cursor_position').text,
            '48 x 48'
        )

        self._getMap(50, 50).getItem().click()
        self.assertEqual(
            self.byCssSelector('.menu_interface .left .cursor_position').text,
            '50 x 50'
        )

        self._moveCursor(self._getMap(48, 48))
        self.assertEqual(
            self.byCssSelector('.menu_interface .left .cursor_position').text,
            '50 x 50'
        )

    def testGetInfo_WithoutSelect(self):
        self._prepareTown()
        self.login()

        self._moveCursor(self._getMap(50, 50))

        interfaceBlock = self.byNg("menuInterface.type == 'towns'", 'ng-show')
        self.assertEqual(
            interfaceBlock.byCss('.type').text,
            'Село - ' + self.town1.getName()
        )
        self.assertEqual(
            interfaceBlock.byCss('.holder > a').text,
            self.user.getLogin()
        )

        self.assertEqual(
            interfaceBlock.byCss('.population').text,
            'Население: 5 000'
        )

        self._moveCursor(self._getMap(48, 48))
        self.assertFalse(
            self.byNg("menuInterface.type == 'towns'", 'ng-show').is_displayed(),
        )