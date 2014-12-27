from selenium.common.exceptions import NoSuchElementException
from . import abstract

class Asserts(abstract.AbstractDeclaration):

    def assertElementExist(self, selector, by='css', parent=None):
        """
        asserting, is element should exist
        """
        if by == 'css':
            try:
                if parent is None:
                    self.byCssSelector(selector)
                else:
                    parent.byCss(selector)

            except NoSuchElementException:
                self.fail(msg='Css selector %s is not exist' % selector)

        elif by == 'xpath':
            try:
                if parent is None:
                    self.byXPath(selector)
                else:
                    parent.byXPath(selector)

            except NoSuchElementException:
                self.fail(msg='XPath %s is not exist' % selector)
        else:
            raise Exception('Select wrong type search')

    def assertElementNotExist(self, selector, by='css'):
        """
        asserting, is element should not exist
        """
        if by == 'css':
            try:
                self.byCssSelector(selector)
                self.fail(msg='Css selector %s is exist' % selector)
            except NoSuchElementException:
                pass

        elif by == 'xpath':
            try:
                self.byXPath(selector)
                self.fail(msg='XPath %s is exist' % selector)
            except NoSuchElementException:
                pass
        else:
            raise Exception('Select wrong type search')
