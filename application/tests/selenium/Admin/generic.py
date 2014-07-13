from tests.selenium import generic


class Selenium_Admin_Generic(generic.Selenium_Generic):
    def _goToAdmin(self):
        self.byCssSelector('.icon_admin').click()
        self.waitForElement('#admin-holder')
