import system.mongo
import pymongo

_db = system.mongo.mongo


def objectId(value):
    return _db.id(value)


def bsonCode(text):
    return _db.code(text)