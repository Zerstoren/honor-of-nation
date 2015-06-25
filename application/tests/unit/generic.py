import unittest


class UnitTest_Generic(unittest.TestCase):
    def setUp(self):
        print("Output -> " + self.__class__.__name__ + " -- " + self._testMethodName)

    def tearDown(self):
        pass
