from tests.generic import Generic
from . import global_actions

import config

from selenium import webdriver
from selenium.webdriver import ActionChains as WebDriverActionChain
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from tests.bootstrap.Selenium import SeleniumFacade

import time
import sys
import subprocess
import random

# Create alias for most popular actions
webdriver.remote.webelement.WebElement.byCss = webdriver.remote.webelement.WebElement.find_element_by_css_selector
webdriver.remote.webelement.WebElement.byXPath = webdriver.remote.webelement.WebElement.find_element_by_xpath
webdriver.remote.webelement.WebElement.byId = webdriver.remote.webelement.WebElement.find_element_by_xpath
webdriver.remote.webelement.WebElement.byClass = webdriver.remote.webelement.WebElement.find_element_by_class_name
webdriver.remote.webelement.WebElement.byCssMany = webdriver.remote.webelement.WebElement.find_elements_by_css_selector
webdriver.remote.webelement.WebElement.byXPathMany = webdriver.remote.webelement.WebElement.find_elements_by_xpath
webdriver.remote.webelement.WebElement.byIdMany = webdriver.remote.webelement.WebElement.find_elements_by_xpath
webdriver.remote.webelement.WebElement.byClassMany = webdriver.remote.webelement.WebElement.find_elements_by_class_name

webdriver.remote.webdriver.WebDriver.byCss = webdriver.remote.webdriver.WebDriver.find_element_by_css_selector
webdriver.remote.webdriver.WebDriver.byXPath = webdriver.remote.webdriver.WebDriver.find_element_by_xpath
webdriver.remote.webdriver.WebDriver.byId = webdriver.remote.webdriver.WebDriver.find_element_by_xpath
webdriver.remote.webdriver.WebDriver.byClass = webdriver.remote.webdriver.WebDriver.find_element_by_class_name
webdriver.remote.webdriver.WebDriver.byCssMany = webdriver.remote.webdriver.WebDriver.find_elements_by_css_selector
webdriver.remote.webdriver.WebDriver.byXPathMany = webdriver.remote.webdriver.WebDriver.find_elements_by_xpath
webdriver.remote.webdriver.WebDriver.byIdMany = webdriver.remote.webdriver.WebDriver.find_elements_by_xpath
webdriver.remote.webdriver.WebDriver.byClassMany = webdriver.remote.webdriver.WebDriver.find_elements_by_class_name


class Selenium_Abstract_Generic(Generic, global_actions.GlobalItems):
    keys = Keys
    managedProcess = None
    isSetup = False

    def setUp(self):
        self.isSetup = True
        super().setUp()

        self.driver = None
        self.driversDict = {}
        self._port = str(random.randint(10000, 65000))

        self.createWindow('main')
        self.useWindow('main')

        if self.managedProcess is not None:
            raise RuntimeError('Game server already started')

        self.managedProcess = subprocess.Popen([
            'python3',
            '-B',
            '%s/init.py' % sys.path[0],
            '--type=test_server',
            '--database=%s' % self.core.database_name,
            '--port=%s' % self._port
        ])

    def tearDown(self):
        self.isSetup = False
        super().tearDown()

        if self.core.remove_core:
            self.closeWindow('ALL')
            self.managedProcess.terminate()
            self.managedProcess = None

    def _executeTestPart(self, function, outcome, isTest=False):
        def testWrapper(*args, **kwargs):
            maxAttempts = int(config.get('testing.retry'))
            attempt = 1

            while True:
                if self.isSetup is False:
                    self.setUp()

                if attempt != maxAttempts:
                    try:
                        function(*args, **kwargs)
                        break

                    except:
                        attempt += 1
                        self.driver.save_screenshot(
                            "/tmp/selenium-error-screen-" + self.__class__.__name__ + "--" + self._testMethodName + '.png'
                        )

                        if self.isSetup is True:
                            self.tearDown()

                else:
                    function(*args, **kwargs)
                    break

        if isTest:
            super()._executeTestPart(testWrapper, outcome, isTest)
        else:
            super()._executeTestPart(function, outcome, isTest)

    def byCssSelector(self, cssSelector):
        return self.driver.byCss(cssSelector)

    def byXPath(self, xpath):
        return self.driver.byXPath(xpath)

    def byNg(self, model, by='ng-model'):
        return self.byXPath('//*[@%(by)s="%(model)s"]' % {
            "model": model,
            "by": by
        })

    def sleep(self, n):
        time.sleep(n)

    def waitForSocket(self, n=10000):
        sleepTime = 0

        while True:
            active = self.executeCommand("return pack('COM.Socket').Counter")

            if active <= 0:
                break
            elif sleepTime >= n:
                break
            else:
                sleepTime += 50
                self.sleep(0.05)

        self.sleep(0.2)

    def go(self, path):
        self.driver.get('http://' + config.get('server.domain') + path)

    def getUrl(self):
        # TODO Change for native driver method
        return self.executeCommand('return location.pathname')

    def executeCommand(self, script):
        return self.driver.execute_script(script, [])

    def createWindow(self, name):
        createDriver = SeleniumFacade()

        createDriver.driver.set_window_size(1366, 4000)
        createDriver.driver.get('http://' + config.get('server.domain') + '/css/style.css')
        createDriver.driver.execute_script("window.localStorage.port = '%s'" % self._port, [])

        self.driversDict[name] = createDriver

    def useWindow(self, name):
        if name not in self.driversDict:
            raise Exception('Driver %s not created' % name)

        self.driver = self.driversDict[name].driver

    def closeWindow(self, name):
        if name == 'ALL':
            for (key, value) in list(self.driversDict.items()):
                self.closeWindow(key)

        elif name in self.driversDict:
            self.driversDict[name].driver.quit()
            del self.driversDict[name]

    def getChainAction(self):
        return WebDriverActionChain(self.driver)

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

    def selectOptionText(self, element, optionText):
        element.byXPath('//option[.="' + optionText + '"]').click()

    def selectOptionValue(self, element, optionValue):
        element.byXPath('//option[@value="' + optionValue + '"]').click()
