from tests.selenium.Main.Menu.Admin import generic
import models.Map.Factory


class Selenium_Main_Menu_Admin_MapTest(generic.Selenium_Main_Menu_Admin_Generic):
    def _setMapFillMethod(self, item=1):
        self.byCssSelector('.change-type-fill > button:nth-child(%d)' % item).click()

    def _setFillLand(self, land, number):
        self.byCssSelector('.fill-items > div:nth-child(%d) button:nth-child(%d)' % \
            (land, number)).click()

    def _setChunkNumber(self, value):
        self.byCssSelector('.fill-type-chunk .sl-select-chunk').clear()
        self.byCssSelector('.fill-type-chunk .sl-select-chunk').send_keys(str(value))

    def _addChunkToList(self):
        self.byCssSelector('.fill-type-chunk .sl-add-to-list').click()

    def _removeChunkFromList(self, chunk):
        self.byXPath('//div//span[.="%s"]/../a' % chunk).click()

    def _fillArea(self):
        self.byCssSelector('.map_fill .sl-fill-area').click()

    def _setChunkX(self, n):
        item = self.byNg('popup.admin.vars.fillChunkPosX')
        item.clear()
        item.send_keys(str(n))

    def _setChunkY(self, n):
        item = self.byNg('popup.admin.vars.fillChunkPosY')
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

    def testMapCreateByChunk(self):
        self.login()

        self._getMenuItem('admin').click()
        self._selectTestAdminBlock('map')

        self._setMapFillMethod(2)

        self._setChunkNumber(1)
        self._addChunkToList()

        self._setChunkNumber(3)
        self._addChunkToList()

        self._removeChunkFromList(3)

        self._setFillLand(1, 1)

        self._fillArea()

        self.waitForSocket()

        # result check
        items = models.Map.Factory.factory.getByChunk(1)
        self.assertEqual(256, len(items))

        items = models.Map.Factory.factory.getByChunk(3)
        self.assertEqual(0, len(items))

    def testMapCreateByChunkCoordinate(self):
        self.login()
        self._getMenuItem('admin').click()
        self._selectTestAdminBlock('map')

        self._setMapFillMethod(2)

        self._setChunkX(1)
        self._setChunkY(1)
        self._addChunkToList()

        self._setChunkX(45)
        self._setChunkY(1)
        self._addChunkToList()

        self._removeChunkFromList(3)

        self._setFillLand(1, 1)

        self._fillArea()

        self.waitForSocket()

        # result check
        items = models.Map.Factory.factory.getByChunk(1)
        self.assertEqual(256, len(items))

        items = models.Map.Factory.factory.getByChunk(3)
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
