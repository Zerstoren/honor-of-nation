import config

import random
import hashlib
import system.mongo
import time


class Core():
    indexName = None

    def __init__(self):
        self.remove_core = True
        self.indexName = self.getRandomName()
        self.database_name = "hn_test_core_" + self.indexName
        config._config[config.configType]['database.mongodb.db'] = self.database_name

        system.mongo.mongo.connection = system.mongo.MongoAbs(self.database_name).connection
        self._mongo = system.mongo.mongo
        self._mongo['test_data'] = {
            'timeCreated': time.time()
        }
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

    def removeOldCores(self):
        for i in system.mongo.mongo.mainConnect.database_names():
            if i.find('hn_test_core') == -1:
                continue

            info = system.mongo.mongo.mainConnect[i]['test_data'].find_one()
            if not info or not info['timeCreated'] or info['timeCreated'] < time.time() - int(config.get('testing.db_cores.remove_time_out')):
                system.mongo.mongo.mainConnect.drop_database(i)
