import config

import random
import hashlib
import system.mongo


class Core():
    indexName = None

    def __init__(self):
        self.remove_core = True
        self.indexName = self.getRandomName()
        self.database_name = "hn_test_core_" + self.indexName
        config._config[config.configType]['database.mongodb.db'] = self.database_name

        system.mongo.mongo.connection = system.mongo.MongoAbs(self.database_name).connection
        self._mongo = system.mongo.mongo
        self.createIndexes()

    def safe_core(self):
        self.remove_core = False

    def destruct(self):
        if self.remove_core:
            self._mongo.mainConnect.drop_database(self.database_name)
        else:
            print("Database %s save in storage" % self.database_name)

    def getRandomName(self, prefix='', length=8):
        return prefix + hashlib.md5(str(random.randint(0, 100000000)).encode()).hexdigest()[0:length]

    def getRandomInt(self, minimal=0, maximal=100, prefix=''):
        return prefix + str(random.randint(minimal, maximal))

    def createIndexes(self):
        mongo = self._mongo.connection

        mongo.map.create_index(
            [
                ('pos_id', 1, )
            ],
            name='Unique_Position',
            unique=True,
        )

        ############### Index for map
        mongo.map_user_visible.create_index(
            [
                ('user_id', 1, ),
                ('pos_id', 1, )
            ],
            name='Unique_Position',
            unique=True
        )
