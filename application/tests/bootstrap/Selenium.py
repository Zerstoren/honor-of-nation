import os

import config

from selenium import webdriver


class SeleniumFacade(object):
    def __init__(self):
        self.driver = None
        if config.get('testing.browser') == 'Chrome':
            chromeConfig = {
                'loggingPrefs': {
                    'browser':'ALL'
                }
            }

            chromedriver = config.get('testing.browser.chrome.chromedriver')
            os.environ["webdriver.chrome.driver"] = chromedriver
            self.driver = webdriver.Chrome(
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

            self.driver = webdriver.Firefox()

        else:
            raise Exception('Selenium browser is not selected')
