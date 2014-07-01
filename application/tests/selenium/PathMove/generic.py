from tests.selenium import generic


class Selenium_PathMove_Generic(generic.Selenium_Generic):
    def _historyBack(self):
        self.executeCommand('history.back()')

    def _historyForward(self):
        self.executeCommand('history.forward()')
