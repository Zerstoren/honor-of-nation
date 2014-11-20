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
            firefoxConfig = {
                'loggingPrefs': {
                    'browser':'ALL'
                }
            }

            self.driver = webdriver.Firefox(capabilities=firefoxConfig)

        else:
            raise Exception('Selenium browser is not selected')
