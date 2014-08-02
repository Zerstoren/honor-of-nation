import unittest
import config

import tests.bootstrap.bootstrap
import tests.bootstrap.core
import tests.bootstrap.CreateBase
import tests.bootstrap.CheckDatabaseIndexes


from tests.mock import Transfer

import models.User.Factory


if config.get('system.pycharm') == 'true':
    tests.bootstrap.bootstrap.removeOldCores()


class Abstract_Generic(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        self.core = tests.bootstrap.core.Core()

        print("Output -> " + self.__class__.__name__ + " -- " + self._testMethodName)
        self.setUpDb()

    def tearDown(self):
        self.fullCleanCache()
        del self.fixture
        self.core.destruct()

    def setUpDb(self, skipDb=False):
        self.fixture = tests.bootstrap.CreateBase.CreateBase()

    def fullCleanCache(self):
        models.User.Factory.User_Factory._cleanIndexes()

    def mockLoad(self, mockName, *args, **kwargs):
        if mockName is 'Transfer':
            return Transfer.TransferMock(*args, **kwargs)

    def _executeTestPart(self, function, outcome, isTest=False):
        def testWrapper(*args, **kwargs):
            function(*args, **kwargs)
            self._testDatabaseValues()

        if isTest:
            super()._executeTestPart(testWrapper, outcome, isTest)
        else:
            super()._executeTestPart(function, outcome, isTest)

    def _testDatabaseValues(self):
        tests.bootstrap.CheckDatabaseIndexes.CheckDatabaseIndexes(
            config.getDatabase()
        )