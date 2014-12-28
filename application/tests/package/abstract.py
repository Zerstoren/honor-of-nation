class AbstractDeclaration(object):
    TimeoutException = Exception
    NoSuchElementException = Exception

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