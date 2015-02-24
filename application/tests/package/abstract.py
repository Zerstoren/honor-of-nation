class AbstractDeclaration(object):
    TimeoutException = Exception
    NoSuchElementException = Exception

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
        pass

    def goAppUrl(self, path):
        pass