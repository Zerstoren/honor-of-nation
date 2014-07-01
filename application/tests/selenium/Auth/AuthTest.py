from tests.selenium.Auth.generic import Selenium_Auth_Generic


class Selenium_Auth_AuthTest(Selenium_Auth_Generic):
    def testLogin_Success(self):
        self._goToLogin()

        self._getLoginButton().send_keys('Zerst')
        self._getPasswordButton().send_keys('123456' + self.keys.RETURN)

        self.assertElementExist('.mpi__block')

    def testLogin_WrongLoginAndPassword(self):
        self._goToLogin()

        self._getLoginButton().send_keys('Zert')
        self._getPasswordButton().send_keys('123321' + self.keys.RETURN)

        self.assertEquals(
            self._getErrorArea().text,
            'Неверный логин или пароль'
        )
