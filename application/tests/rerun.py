import config

def retry(retry=None):
    def wrapp(f):
        def testWrapper(self, *args, **kwargs):
            maxAttempts = retry or int(config.get('testing.retry'))
            attempt = 1

            while True:
                if self.isSetup is False:
                    self.setUp()

                if attempt != maxAttempts:
                    try:
                        f(self, *args, **kwargs)
                        break

                    except:
                        print("Rerun test. Attempt %i of %i" % (attempt, maxAttempts, ))
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
