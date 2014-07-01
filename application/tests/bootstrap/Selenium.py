import os

import config

from selenium import webdriver


class SeleniumFacade(object):
    def __init__(self):
        self.driver = None

        if config.get('testing.browser') == 'Chrome':
            chromedriver = config.get('testing.browser.chrome.chromedriver')
            os.environ["webdriver.chrome.driver"] = chromedriver
            self.driver = webdriver.Chrome(chromedriver)

        elif config.get('testing.browser') == 'Firefox':
            self.driver = webdriver.Firefox()

        else:
            raise Exception('Selenium browser is not selected')
