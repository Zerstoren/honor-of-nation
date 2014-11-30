from tests.selenium import generic


class Selenium_Town_Generic(generic.Selenium_Generic):
    def openTown(self, town):
        self.goAppUrl('/town/' + str(town.getId()))
        self.sleep(25)
        self.waitForElement('#map-body-holder > .town .content')

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

    def _getBuildsList(self, n):
        pass
        # return self.byCssSelector('.')
