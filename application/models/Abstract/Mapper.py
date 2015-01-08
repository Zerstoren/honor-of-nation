import abc
import system.mongo
import models.Abstract.Common
import exceptions.database

import system.log


class Abstract_Mapper(metaclass=abc.ABCMeta):
    _table = 'towns_builds'

    def __init__(self):
        self._db = system.mongo.mongo
        self._bulk = None
        if self._table is None:
            raise Exception('Mapper %s not define _table' % self.__class__.__name__)

    def _getCollection(self):
        return self._db[self._table] if not self._bulk else self._bulk

    def _select(self, where=None, limit=None, sort=None):
        where = where if where is not None else models.Abstract.Common.Common_Filter()
        limit = limit if limit is not None else models.Abstract.Common.Common_Limit()

        if limit.isOneRecord():
            action = self._getCollection().find_one(where)
            if action is None:
                system.log.info('Data not found in collection %s by query %s' % (self._table, str(where)))
                raise exceptions.database.NotFound('Data not found by ' + str(where))

            return action

        action = self._getCollection().find(where, sort=sort)

        if limit.hasLimit():
            action = action.limit(*limit.getLimit())

        return action

    def _insert(self, data):
        """
        :type data: models.Abstract.Set.Common_Set
        """
        data.add('remove', 0)

        return self._getCollection().insert(data)

    def _update(self, data, filters):
        """
        :type data: models.Abstract.Set.Common_Set
        :type filters: models.Abstract.Filter.Common_Filter
        """
        return self._getCollection().update(filters, {"$set": data})

    def _remove(self, queryId):
        """
        :type queryId: int
        """
        self._update(
            models.Abstract.Common.Common_Set({'remove': 1}),
            models.Abstract.Common.Common_Filter({'_id': queryId})
        )

    def remove(self, domain):
        """
        :type domain: models.Abstract.Domain.Abstract_Domain
        """
        self._remove(
            domain.getId()
        )

    def bulkStart(self):
        self._bulk = self._db[self._table].initialize_unordered_bulk_op()

    def bulkEnd(self):
        try:
            result = self._getCollection().execute()
        except system.mongo.exceptions.InvalidOperation as e:
            result = None
        finally:
            self._bulk = None

        return result

    def getById(self, queryId):
        result = self._select(
            models.Abstract.Common.Common_Filter().setId(queryId),
            models.Abstract.Common.Common_Limit().setOne()
        )

        if result is None:
            raise exceptions.database.NotFound('Data by _id %s not found in table `%s`' % (queryId, self._table))

        return result

    def getByIds(self, ids):
        commonFilter = models.Abstract.Common.Common_Filter()
        commonFilter.addIn('_id', ids)

        return self._select(commonFilter)

    def _objectId(self, value):
        return self._db.id(value)

    def _bsonCode(self, text):
        return self._db.code(text)