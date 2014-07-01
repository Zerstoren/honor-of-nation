from tests import generic


class UnitTest_Generic(generic.Generic):
    def setUp(self):
        print("Output -> " + self.__class__.__name__ + " -- " + self._testMethodName)

    def tearDown(self):
        pass
