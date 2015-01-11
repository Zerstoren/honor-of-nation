from tests.selenium import generic


class Selenium_Town_Generic(generic.Selenium_Generic):
    # BUILDS
    def _getBuildElement(self, key):
        return self.byCssSelector('#' + key + ' .name img')

    def _getSelectorBuild(self):
        return '.list_of_progress_builds .buildInProgress'

    def _getCurrentBuild(self):
        return self.byCssSelector(self._getSelectorBuild())

    def _getCurrentBuildName(self):
        return self._getCurrentBuild().byCss('.name .build-name').text

    def _getCurrentBuildLevel(self):
        return self._getCurrentBuild().byCss('.name .build-level').text

    def _showUnitPopup(self, unitEquipment):
        chain = self.getChainAction()
        chain.move_to_element(self.byCssSelector('.units_container[data-id="%s"]' % str(unitEquipment.getId())))
        chain.perform()
        self.sleep(1)

    def _createUnit(self, unitEquipment, count):
        self._showUnitPopup(unitEquipment)
        unit = self.byCssSelector('.units_container[data-id="%s"]' % str(unitEquipment.getId()))
        unit.byCss('.count_to_create').clear()
        unit.byCss('.count_to_create').send_keys(str(count))
        unit.byCss('.create').click()

        self.waitForElement('.buildInProgress .name')
