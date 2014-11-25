from tests.generic import Generic

import config

from selenium import webdriver
from selenium.webdriver import ActionChains as WebDriverActionChain
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By as WebDriverCommonBy
import selenium.webdriver.support.expected_conditions as WebDriverExpectedCondition
import selenium.webdriver.support.ui as WebDriverUI

from tests.bootstrap.Selenium import SeleniumFacade

import time
import sys
import subprocess
import signal
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


class Selenium_Abstract_Generic(Generic):
    keys = Keys
    managedProcess = None
    isSetup = False

    TimeoutException = TimeoutException
    NoSuchElementException = NoSuchElementException

    def setUp(self):
        self.isSetup = True
        super().setUp()

        self.driver = None
        self.driversDict = {}
        self._port = 36450
        self._balancer_port = 36451

        self.createWindow('main')
        self.useWindow('main')

        if self.managedProcess is not None:
            raise RuntimeError('Game server already started')

        basePath = sys.path[1]

        if config.configType == 'jankins_test':
            basePath = sys.path[0]

        print("Start process")
        self.managedProcess = subprocess.Popen([
                'python3',
                '-B',
                '%s/init_balancer.py' % basePath,
                '--type=%s' % config.configType,
                '--database=%s' % self.core.database_name,
                '--port=%s' % self._port,
                '--balancer_port=%s' % self._balancer_port
            ],
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        print("Process with pid " + str(self.managedProcess.pid))

    def tearDown(self):
        self.isSetup = False
        super().tearDown()

        # if self.core.remove_core:
        self.closeWindow('ALL')

        subprocess.call("pkill -TERM -P " + str(self.managedProcess.pid))
        subprocess.call("kill -TERM " + str(self.managedProcess.pid))
        print("Kill pricess" + str(self.managedProcess.pid))

        # self.managedProcess.send_signal(signal.SIGINT)
        # print(self.managedProcess.communicate(), self.managedProcess.returncode)

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

    def byAttribute(self, attr, value):
        return self.byXPath('//*[@%(attr)s="%(value)s"]' % {
            "attr": attr,
            "value": value
        })

    def sleep(self, n):
        time.sleep(n)

    def waitForElement(self, selector, by='css'):
        waiter = WebDriverUI.WebDriverWait(self.driver, int(config.get('testing.waitUtilTime')))

        if by == 'css':
            waiter.until(WebDriverExpectedCondition.visibility_of_element_located(
                (WebDriverCommonBy.CSS_SELECTOR, selector))
            )
        elif by == 'xpath':
            waiter.until(WebDriverExpectedCondition.visibility_of_element_located(
                (WebDriverCommonBy.XPATH, selector))
            )

    def waitForSocket(self, n=10000):
        sleepTime = 0

        while True:
            active = self.executeCommand("return require('system/socket').counter;")

            if active != None and active <= 0:
                break
            elif sleepTime >= n:
                raise TimeoutException("Very long wait for socket")
            else:
                sleepTime += 500
                self.sleep(0.5)


    def go(self, path):
        self.driver.get('http://' + config.get('server.domain') + path)

    def goAppUrl(self, path):
        self.executeCommand("""
        requirejs(['system/route'], function(router){
            router.navigate('%s')
        });
        """ % path)

    def waitForUserLogin(self):
        def getUserLogin():
            return self.executeCommand("return require('service/standalone/user').me.get('login')")

        i = 0
        while True:
            i += 1
            s = getUserLogin()

            if s != None:
                break
            elif i >= 100:
                raise TimeoutException('Can`t login')

            self.sleep(0.05)

    def getUrl(self):
        # TODO Change for native driver method
        return self.executeCommand('return location.pathname')

    def executeCommand(self, script):
        return self.driver.execute_script(script, [])

    def createWindow(self, name):
        createDriver = SeleniumFacade()

        createDriver.driver.set_window_size(1366, 1000)
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
