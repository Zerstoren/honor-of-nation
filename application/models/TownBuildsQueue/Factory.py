import models.Abstract.Factory
import exceptions.database

from . import Domain
from . import Mapper


class TownBuildsQueue_Factory_Main(models.Abstract.Factory.Abstract_Factory):
    def getDomainByTownAndKey(self, townDomain, key):
        try:
            result = Mapper.TownBuildsQueue_Mapper.getByTownAndKey(townDomain, key)
        except exceptions.database.NotFound:
            result = None

        if result:
            return self.getDomainFromData(result)
        else:
            domain = Domain.TownBuildsQueue_Domain()
            domain.setTown(townDomain)
            domain.setKey(key)

            return domain

    def getDomainFromData(self, result):
        data = {}
        levels = []

        for i in result:
            levels.append(i['level'])

        domain = Domain.TownBuildsQueue_Domain()
        domain.setOptions({

        })

        return domain

TownBuildsQueue_Factory = TownBuildsQueue_Factory_Main()
