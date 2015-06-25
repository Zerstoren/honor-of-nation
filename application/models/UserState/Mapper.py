import models.Abstract.Mapper
from . import Common


class UserState_Mapper_Main(models.Abstract.Mapper.Abstract_Mapper):
    _table = 'users_state'

    def save(self, domain):
        self.updateBaseState(
            domain.getFrom(),
            domain.getTo(),
            domain.getState()
        )

    def userStates(self, user):
        commonFilter = Common.Common_Filter()
        commonFilter.add('from', user.getId())

        return self._select(commonFilter)

    def userState(self, fromUser, toUser):
        commonFilter = Common.Common_Filter()
        commonFilter.add('from', fromUser.getId())
        commonFilter.add('to', toUser.getId())

        commonLimit = Common.Common_Limit()
        commonLimit.setOne()

        return self._select(commonFilter, commonLimit)

    def createBaseState(self, fromUser, toUser):
        commonSet = Common.Common_Filter()
        commonSet.add('from', fromUser.getId())
        commonSet.add('to', toUser.getId())
        commonSet.add('state', Common.STATE_NEUTRAL)

        self._insert(commonSet)

        commonSet = Common.Common_Filter()
        commonSet.add('to', fromUser.getId())
        commonSet.add('from', toUser.getId())
        commonSet.add('state', Common.STATE_NEUTRAL)

        self._insert(commonSet)

    def updateBaseState(self, fromUser, toUser, state):
        assert state in [
            Common.STATE_ALLIANCE,
            Common.STATE_UNION,
            Common.STATE_TRADE,
            Common.STATE_NEUTRAL,
            Common.STATE_WAR,
        ]

        first = self.userState(fromUser, toUser)
        second = self.userState(toUser, fromUser)

        commonFilter = Common.Common_Filter()
        commonFilter.setId(first['_id'])
        commonSet = Common.Common_Set()
        commonSet.add('state', state)
        self._update(commonSet, commonFilter)

        commonFilter = Common.Common_Filter()
        commonFilter.setId(second['_id'])
        commonSet = Common.Common_Set()
        commonSet.add('state', state)
        self._update(commonSet, commonFilter)

        return True


UserState_Mapper = UserState_Mapper_Main()
