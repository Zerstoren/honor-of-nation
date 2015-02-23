import models.Abstract.Factory

from . import Domain
from . import Mapper


class TownBonus_Factory_Main(models.Abstract.Factory.Abstract_Factory):
    def get(self, town):
        result = Mapper.TownBonus_Mapper.get(town)
        domain = Domain.TownBonus_Domain()
        domain.setOptions(result)

        return domain

TownBonus_Factory = TownBonus_Factory_Main()
