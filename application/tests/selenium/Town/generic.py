from tests.selenium import generic
from tests.package.asserts import Asserts
from tests.package.dom import Dom


class Selenium_Town_Generic(
    generic.Selenium_Generic,
    Dom,
    Asserts
):
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

        self.waitForElement('.unit-item')

    def _getArmyInList(self, armyDomain):
        return self.byCssSelector('.listUnits .units li[data-id="%s"] img' % str(armyDomain.getId()))

    def _selectArmyInList(self, armyDomain):
        self._getArmyInList(armyDomain).click()

    def _armyNotInList(self, armyDomain):
        self.waitForElementHide('.listUnits .units li[data-id="%s"]' % str(armyDomain.getId()))

    def _armyAction(self, action):
        self.byCssSelector('.listUnits .actions li.%s:not(.disabled)' % action).click()

    def _isArmyActionDisabled(self, action):
        self.byCssSelector('.listUnits .actions li.%s.disabled' % action)

    def _openCommanderDetail(self, armyDomain):
        self.rightClick(self._getArmyInList(armyDomain))
        self.waitForElementHide('.waiting')

    def _getArmyInDetail(self, armyDomain, atElement=None):
        query = '*[data-id="%s"] img' % str(armyDomain.getId())

        if atElement:
            return atElement.byCss(query)
        else:
            return self.byCssSelector('.popover.unit-detail ' + query)

    def _armyNotShowInDetail(self, armyDomain):
        self.assertElementNotExist('.popover.unit-detail *[data-id="%s"]' % str(armyDomain.getId()))

    def _getBuffer(self):
        return self.byCssSelector('.popover.unit-detail .buffer ul')

    def _getMiddleSuite(self):
        return self.byCssSelector('.popover.unit-detail .suite-target-middleware')

    def _getBottomSuite(self):
        return self.byCssSelector('.popover.unit-detail .suite-target-downware')

    def _getMiddleUnitsList(self):
        return self.byCssSelector('.popover.unit-detail .commander-units-list')

    def _getBottomUnitsList(self):
        return self.byCssSelector('.popover.unit-detail .general-units-list')
