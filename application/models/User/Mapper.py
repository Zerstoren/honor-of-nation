from jinja2._stringdefs import Co
import models.Abstract.Mapper
import exceptions.database
from . import Common


class User_Mapper_Main(models.Abstract.Mapper.Abstract_Mapper):
    _table = 'users'
    _transfer = None

    def getByLogin(self, login):
        limit = Common.Common_Limit().setOne()
        where = Common.Common_Filter({'login': login})

        result = self._select(where, limit)

        if result is None:
            raise exceptions.database.NotFound('User by login %s not found' % login)

        return result

    def save(self, domain):
        commonSet = Common.Common_Set()

        commonSet\
            .add('login', domain.getLogin())\
            .add('password', domain.getPassword())\
            .add('admin', domain.getAdmin())\
            .add('position', domain.getPosition())

        if domain.hasId():
            self._update(
                commonSet,
                Common.Common_Filter({'_id': domain.getId()})
            )
        else:
            cursor = self._insert(commonSet)
            domain.setId(cursor)

    def searchUser(self, login):
        commonFilter = Common.Common_Filter()
        commonFilter.add('login', login)

        commonLimit = Common.Common_Limit()
        commonLimit.setOne()

        return self._select(commonFilter, commonLimit)

    def getAllUsersLogin(self):
        return self._getCollection().find({}, {'_id': 1, 'login': 1})


User_Mapper = User_Mapper_Main()
