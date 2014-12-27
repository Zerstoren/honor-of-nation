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
import os.path
import subprocess
import signal
import random

import logging
selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
selenium_logger.setLevel(logging.WARNING)

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


class Selenium_Generic(Generic):
    execution = 'selenium'

    keys = Keys
    managedProcess = None

    TimeoutException = TimeoutException
    NoSuchElementException = NoSuchElementException

    def setUp(self):
        self._port = random.randint(10000, 65000)
        self._balancer_port = self._port + 1
        super().setUp()

        if self.managedProcess is not None:
            raise RuntimeError('Game server already started')

        self.managedProcess = subprocess.Popen([
                'python3',
                '-B',
                'init_balancer.py',
                '--type=%s' % config.configType,
                '--database=%s' % self.core.database_name,
                '--port=%s' % self._port,
                '--balancer_port=%s' % self._balancer_port
            ],
           cwd=str(os.path.dirname(os.path.realpath(__file__))) + '/../../'
           # ,stderr=subprocess.PIPE,
           # stdout=subprocess.PIPE
        )

        self.driver = None
        self.driversDict = {}

        self.createWindow('main')
        self.useWindow('main')


    def tearDown(self):
        if self.core.remove_core:
            self.closeWindow('ALL')
            self.managedProcess.send_signal(signal.SIGINT)

            self.managedProcess = None

        super().tearDown()
        self.sleep(2)

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

    def waitForElementHide(self, selector, by='css'):
        waiter = WebDriverUI.WebDriverWait(self.driver, int(config.get('testing.waitUtilTime')))

        if by == 'css':
            waiter.until(WebDriverExpectedCondition.invisibility_of_element_located(
                (WebDriverCommonBy.CSS_SELECTOR, selector))
            )
        elif by == 'xpath':
            waiter.until(WebDriverExpectedCondition.invisibility_of_element_located(
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

    def login(self, userDomain=None):
        if userDomain:
            user = userDomain
        else:
            user = self.fixture.getUser(0)

        self.executeCommand("window.localStorage.authLogin = '%s'" % user.getLogin())
        self.executeCommand("window.localStorage.authPassword = '%s'" % user._domain_data['_testPassword'])

        self.go('/')
        self.waitForElement('.mpi__resource_wrapper', 'css')
        self.waitForUserLogin()
        self.waitForElementHide('.connect-is-not-estabilished .text')
        self.waitForElementHide('.connect-is-estabilished .text')

        return user
