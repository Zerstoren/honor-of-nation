from tests.selenium.Main import generic


class Selenium_Main_Menu_Generic(generic.Selenium_Main_Generic):
    def _getMenuItem(self, name):
        return self.byCssSelector('.mpi__menu .icon_' + name)
