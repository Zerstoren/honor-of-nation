import models.Abstract.Mapper
from . import Common


class Army_Mapper_Main(models.Abstract.Mapper.Abstract_Mapper):
    _table = 'army'

    def getByPosition(self, user, position, detail=False):
        commonFilter = Common.Common_Filter()
        commonFilter.add('user', user.getId())
        commonFilter.add('location', position.getPosId())

        if detail:
            commonFilter.add('commander', None)

        return self._select(commonFilter)

    def getSubGenerals(self, generalDomain):
        commonFilter = Common.Common_Filter()
        commonFilter.add('commander', generalDomain.getId())
        commonFilter.add('is_general', True)

        return self._select(commonFilter)

    def getByGeneral(self, generalDomain):
        commonFilter = Common.Common_Filter()
        commonFilter.add('commander', generalDomain.getId())

        return self._select(commonFilter)

    def save(self, unit):
        """
        :type unit: models.Army.Domain.Army_Domain
        """
        commonSet = Common.Common_Set()
        commonSet.add('user', unit.getUser().getId())
        commonSet.add('unit', unit.getUnit().getId())
        commonSet.add('suite', unit.getSuite().getId() if unit.getSuite() else None)
        commonSet.add('commander', unit.getCommander().getId() if unit.getCommander() else None)
        commonSet.add('count', unit.getCount())
        commonSet.add('location', unit.getMap().getPosition().getPosId())
        commonSet.add('in_build', unit.getInBuild())
        commonSet.add('power', unit.getPower())
        commonSet.add('mode', unit.getMode())
        commonSet.add('move_path', unit.getMovePath())
        commonSet.add('formation', unit.getFormation())
        commonSet.add('is_general', unit.getIsGeneral())

        if unit.hasId():
            commonFilter = Common.Common_Filter()
            commonFilter.setId(unit.getId())
            self._update(commonSet, commonFilter)
        else:
            insertId = self._insert(commonSet)
            unit.setId(insertId)

        return unit



Army_Mapper = Army_Mapper_Main()
