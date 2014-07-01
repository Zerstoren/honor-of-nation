#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.selenium.generic import Selenium_Generic


class Selenium_Auth_Generic(Selenium_Generic):
    def _goToLogin(self):
        self.go('/login')

    def _getLoginButton(self):
        return self.byCssSelector('.auth .auth__input_login')

    def _getPasswordButton(self):
        return self.byCssSelector('.auth .auth__input_password')

    def _getErrorArea(self):
        return self.byCssSelector('.auth__error')
