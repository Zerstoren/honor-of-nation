import abc
import system.mongo
import models.Abstract.Common
import exceptions.database


class Abstract_Mapper(metaclass=abc.ABCMeta):
    _table = None

    def __init__(self):
        self._db = system.mongo.mongo
        if self._table is None:
            raise Exception('Mapper %s not define _table' % self.__class__.__name__)

    def _select(self, where=None, limit=None):
        """
        :type where: models.Abstract.Filter.Common_Filter
        :type limit: models.Abstract.Limit.Common_Limit
        """
        where = where if where is not None else models.Abstract.Common.Common_Filter()
        limit = limit if limit is not None else models.Abstract.Common.Common_Limit()

        if limit.isOneRecord():
            action = self._db[self._table].find_one(where)
            if action is None:
                raise exceptions.database.NotFound('Data not found by ' + str(where))

            return action

        action = self._db[self._table].find(where)

        if limit.hasLimit():
            action = action.limit(*limit.getLimit())

        return action

    def _insert(self, data):
        """
        :type data: models.Abstract.Set.Common_Set
        """
        data.add('remove', 0)

        return self._db[self._table].insert(data, manipulate=True)

    def _update(self, data, filters):
        """
        :type data: models.Abstract.Set.Common_Set
        :type filters: models.Abstract.Filter.Common_Filter
        """
        return self._db[self._table].update(filters, {"$set": data})

    def _remove(self, queryId):
        """
        :type queryId: int
        """
        self._update(
            models.Abstract.Common.Common_Set({'remove': 1}),
            models.Abstract.Common.Common_Filter({'_id': queryId})
        )

    def getById(self, queryId):
        result = self._select(
            models.Abstract.Common.Common_Filter().setId(queryId),
            models.Abstract.Common.Common_Limit().setOne()
        )

        if result is None:
            raise exceptions.database.NotFound('Data by _id %s not found in table `%s`' % (queryId, self._table))

        return result

    def _objectId(self, value):
        return self._db.id(value)

    def _bsonCode(self, text):
        return self._db.code(text)