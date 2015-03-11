import os

import config

from selenium import webdriver


class SeleniumFacade(object):
    def __init__(self):
        self.driver = None
        self.driversDict = {}

    def _createWindow(self, name):
        if config.get('testing.browser') == 'Chrome':
            chromeConfig = {
                'loggingPrefs': {
                    'browser':'ALL'
                }
            }

            chromedriver = config.get('testing.browser.chrome.chromedriver')
            os.environ["webdriver.chrome.driver"] = chromedriver

            return webdriver.Chrome(
                chromedriver
            )

        elif config.get('testing.browser') == 'Firefox':
            # firefoxConfig = {
            #     'loggingPrefs': {
            #         'browser':'ALL'
            #     }
            # }
            # firefoxProfile = webdriver.FirefoxProfile()
            # firefoxProfile.set_preference("browser.cache.disk.capacity", 0)
            # firefoxProfile.set_preference("browser.cache.disk.smart_size.first_run", False)
            # firefoxProfile.set_preference("browser.cache.disk.smart_size.use_old_max", False)
            # firefoxProfile.set_preference("browser.cache.disk.smart_size_cached_value", 0)
            # firefoxProfile.set_preference("browser.cache.disk.enable", False)
            # firefoxProfile.set_preference("browser.cache.memory.enable", False)
            # firefoxProfile.set_preference("browser.cache.offline.enable", False)
            # firefoxProfile.set_preference("network.http.use-cache", False)

            return webdriver.Firefox()

        else:
            raise Exception('Selenium browser is not selected')

    def createWindow(self, name):
        if name in self.driversDict:
            raise Exception('Driver %s already created' % name)

        createDriver = self._createWindow(name)
        self.driversDict[name] = createDriver

    def updateWindowSetting(self, name, port):
        driver = self.driversDict[name]

        driver.set_window_size(1366, 1000)
        driver.get('http://' + config.get('server.domain') + '/css/style.css')
        driver.execute_script("window.localStorage.port = '%s'" % port, [])

    def getWindow(self, name):
        if name not in self.driversDict:
            raise Exception('Driver %s not created' % name)

        return self.driversDict[name]

    def closeWindow(self, name):
        if name == 'ALL':
            for (key, value) in list(self.driversDict.items()):
                self.closeWindow(key)

        elif name in self.driversDict:
            self.driversDict[name].quit()
            del self.driversDict[name]

SeleniumFacadeInstance = SeleniumFacade()