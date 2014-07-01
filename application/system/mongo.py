import config
import inspect

import pymongo
import bson


class NotFound(pymongo.errors.PyMongoError):
    pass


class exceptions(object):
    NotFound = NotFound
    Duplicate = pymongo.errors.DuplicateKeyError
    InvalidId = bson.errors.InvalidId


class types(object):
    ObjectId = bson.objectid.ObjectId


def cleanObjectId(target):
    if isinstance(target, types.ObjectId):
        return str(target)

    elif isinstance(target, dict):
        map(cleanObjectId, target)

    elif isinstance(target, list):
        map(cleanObjectId, target)

    elif inspect.isclass(target):
        return str(target)

    else:
        return target


class MongoAbs(dict):
    def __init__(self, database_name=False):
        super().__init__()

        self.mainConnect = pymongo.MongoClient(config.get('database.mongodb.connect'))
        self.connection = \
            self.mainConnect[database_name if database_name else config.get('database.mongodb.db')]

    def __getitem__(self, collection):
        return self.connection[collection]

    def __getattr__(self, collection):
        return self.connection[collection]

    def id(self, idString):
        try:
            return bson.objectid.ObjectId(idString)
        except bson.errors.InvalidId:
            return False

    def code(self, fn):
        return bson.code.Code(fn)

    def _close_connection(self):
        pass

mongo = MongoAbs()
