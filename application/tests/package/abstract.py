from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains as WebDriverActionChain

class AbstractDeclaration(object):
    TimeoutException = Exception
    NoSuchElementException = Exception
    keys = Keys

    def sleep(self, n):
        pass

    def getRandomInt(self, minimal=0, maximal=100, prefix=''):
        pass

    def getRandomName(self, prefix='', length=8):
        pass

    def waitForElement(self, selector, by='css'):
        pass

    def waitForElementHide(self, selector, by='css'):
        pass

    def byCssSelector(self, selector):
        pass

    def byXPath(self, selector):
        pass

    def fail(self, msg):
        pass

    def getChainAction(self):
        return WebDriverActionChain(None)

    def goAppUrl(self, path):
        pass

    def executeCommand(self, script, *args):
        pass
