from tests.selenium.Main.Menu import generic


class Selenium_Main_Menu_Admin_Generic(generic.Selenium_Main_Menu_Generic):
    def _selectTestAdminBlock(self, name):
        self.byCssSelector('#popup-admin-select-' + name).click()
        self.waitForSocket()

    def _resourceCreateButton(self):
        return self.byNg('popup.admin.func.resourceCreate()', by='ng-click')
