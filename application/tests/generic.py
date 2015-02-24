import unittest
import config
import hashlib
import random

import tests.bootstrap.bootstrap
import tests.bootstrap.core
import tests.bootstrap.CreateBase
import tests.bootstrap.CheckDatabaseIndexes


from tests.mock import Transfer

import models.User.Factory

import pprint

from tests.package.db.user import User
from tests.package.db.terrain import Terrain

class Generic(
    unittest.TestCase,
    User,
    Terrain
):
    maxDiff = None
    isSetup = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def print(self, *args, **kwargs):
        pprint.pprint(*args, **kwargs)

    def setUp(self):
        self.isSetup = True
        self.core = tests.bootstrap.core.Core()

        print("Output -> " + self.__class__.__name__ + " -- " + self._testMethodName)
        self.setUpDb()

    def tearDown(self):
        self.isSetup = False
        try:
            self._testDatabaseValues()
        except Exception as e:
            raise e
        finally:
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

    def _testDatabaseValues(self):
        tests.bootstrap.CheckDatabaseIndexes.CheckDatabaseIndexes(
            config.getDatabase()
        )

    def getRandomName(self, prefix='', length=8):
        return prefix + hashlib.md5(str(random.randint(0, 100000000)).encode()).hexdigest()[0:length]

    def getRandomInt(self, minimal=0, maximal=100, prefix=''):
        return prefix + str(random.randint(minimal, maximal)) if prefix else random.randint(minimal, maximal)
