import models.Abstract.Domain
from .Mapper import BattleAsk_Mapper


class BattleAsk_Domain(models.Abstract.Domain.Abstract_Domain):
    def getMapper(self):
        """
        required method, for IDE static analyzer
        """
        return BattleAsk_Mapper
