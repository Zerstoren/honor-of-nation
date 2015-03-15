import config

def retry(retry=None):
    def setUpMethod(self, maxAttempts):
        if self.isSetup:
            return

        attempt = 1

        while True:
            if attempt != maxAttempts:
                try:
                    self.setUp()
                    break

                except Exception:
                    attempt += 1

                    if self.isSetup is True:
                        self.tearDown()

            else:
                self.setUp()
                break


    def wrapp(f):
        def testWrapper(self, *args, **kwargs):
            maxAttempts = retry or int(config.get('testing.retry'))
            attempt = 1

            while True:
                setUpMethod(self, maxAttempts)

                if attempt != maxAttempts:
                    try:
                        f(self, *args, **kwargs)
                        break

                    except Exception:
                        attempt += 1
                        if self.execution == 'selenium':
                            self.driver.get_screenshot_as_file(
                                "/tmp/selenium-error-screen-" + self.__class__.__name__ + "--" + self._testMethodName + '.png'
                            )

                        if self.isSetup is True:
                            self.tearDown()

                else:
                    f(self, *args, **kwargs)
                    break

        return testWrapper

    return wrapp
