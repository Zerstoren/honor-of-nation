from tests.selenium.Main.Menu.Admin import generic
import models.Map.Factory


class Selenium_Main_Menu_Admin_MapTest(generic.Selenium_Main_Menu_Admin_Generic):
    def _setMapFillMethod(self, item=1):
        self.byCssSelector('.change-type-fill > button:nth-child(%d)' % item).click()

    def _setFillLand(self, land, number):
        self.byCssSelector('.fill-items > div:nth-child(%d) button:nth-child(%d)' % \
            (land, number)).click()

    def _setChankNumber(self, value):
        self.byCssSelector('.fill-type-chank .sl-select-chank').clear()
        self.byCssSelector('.fill-type-chank .sl-select-chank').send_keys(str(value))

    def _addChankToList(self):
        self.byCssSelector('.fill-type-chank .sl-add-to-list').click()

    def _removeChankFromList(self, chank):
        self.byXPath('//div//span[.="%s"]/../a' % chank).click()

    def _fillArea(self):
        self.byCssSelector('.map_fill .sl-fill-area').click()

    def _setChankX(self, n):
        item = self.byNg('popup.admin.vars.fillChankPosX')
        item.clear()
        item.send_keys(str(n))

    def _setChankY(self, n):
        item = self.byNg('popup.admin.vars.fillChankPosY')
        item.clear()
        item.send_keys(str(n))

    def _setPositionFromX(self, n):
        item = self.byNg('popup.admin.vars.fillFromPosX')
        item.clear()
        item.send_keys(str(n))

    def _setPositionFromY(self, n):
        item = self.byNg('popup.admin.vars.fillFromPosY')
        item.clear()
        item.send_keys(str(n))

    def _setPositionToX(self, n):
        item = self.byNg('popup.admin.vars.fillToPosX')
        item.clear()
        item.send_keys(str(n))

    def _setPositionToY(self, n):
        item = self.byNg('popup.admin.vars.fillToPosY')
        item.clear()
        item.send_keys(str(n))

    def testMapCreateByChank(self):
        self.login()

        self._getMenuItem('admin').click()
        self._selectTestAdminBlock('map')

        self._setMapFillMethod(2)

        self._setChankNumber(1)
        self._addChankToList()

        self._setChankNumber(3)
        self._addChankToList()

        self._removeChankFromList(3)

        self._setFillLand(1, 1)

        self._fillArea()

        self.waitForSocket()

        # result check
        items = models.Map.Factory.factory.getByChank(1)
        self.assertEqual(256, len(items))

        items = models.Map.Factory.factory.getByChank(3)
        self.assertEqual(0, len(items))

    def testMapCreateByChankCoordinate(self):
        self.login()
        self._getMenuItem('admin').click()
        self._selectTestAdminBlock('map')

        self._setMapFillMethod(2)

        self._setChankX(1)
        self._setChankY(1)
        self._addChankToList()

        self._setChankX(45)
        self._setChankY(1)
        self._addChankToList()

        self._removeChankFromList(3)

        self._setFillLand(1, 1)

        self._fillArea()

        self.waitForSocket()

        # result check
        items = models.Map.Factory.factory.getByChank(1)
        self.assertEqual(256, len(items))

        items = models.Map.Factory.factory.getByChank(3)
        self.assertEqual(0, len(items))

    def testMapCreate_BySelection(self):
        self.login()
        self._getMenuItem('admin').click()
        self._selectTestAdminBlock('map')

        self._setMapFillMethod(1)

        self._setPositionFromX(0)
        self._setPositionFromY(0)

        self._setPositionToX(17)
        self._setPositionToY(17)

        self._setFillLand(1, 1)

        self._fillArea()

        self.waitForSocket()

        # result check
        items = models.Map.Factory.factory.getBySelection(0, 0, 17, 17)
        self.assertEqual(17 * 17, len(items))
