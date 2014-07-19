import models.Abstract.Mapper
import exceptions.database
from . import Common


class Resources_Mapper_Main(models.Abstract.Mapper.Abstract_Mapper):
    _table = 'users_resources'

    def getByUser(self, userDomain):
        where = Common.Common_Filter()
        where.add('user', self._objectId(userDomain.getId()))

        limit = Common.Common_Limit().setOne()
        result = self._select(where, limit)
        if result is None:
            raise exceptions.database.NotFound('User %s dont have resource records' % userDomain.getLogin())

        return result

    def save(self, resourceDomain):
        commonSet = Common.Common_Set()
        commonSet\
            .add('user', resourceDomain.getUser().getId())\
            .add('rubins', resourceDomain.getRubins())\
            .add('wood', resourceDomain.getWood())\
            .add('steel', resourceDomain.getSteel())\
            .add('stone', resourceDomain.getStone())\
            .add('eat', resourceDomain.getEat())\
            .add('gold', resourceDomain.getGold())

        if resourceDomain.hasId():
            self._update(
                commonSet,
                Common.Common_Filter({'_id': resourceDomain.getId()})
            )
        else:
            cursor = self._insert(commonSet)
            resourceDomain.setId(cursor)


Resources_Mapper = Resources_Mapper_Main()
