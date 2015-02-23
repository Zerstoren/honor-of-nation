import models.Town.Domain
import helpers.MapCoordinate
import models.TownBuilds.Factory
import models.TownBuilds.Mapper

from service.TownBonus import Service_TownBonus
from service.TownResources import Service_TownResources


class Town(object):
    def addTown(self, x, y, user, population=None, typeTown=0, name=None):
        population = population if population else self.getRandomInt(100, 10000)
        name = name if name else self.getRandomName('city-')
        mapCoordinate = helpers.MapCoordinate.MapCoordinate(x=x, y=y)

        domain = models.Town.Domain.Town_Domain()
        domain.setPosId(mapCoordinate.getPosId())
        domain.setName(name)
        domain.setType(typeTown)
        domain.setPopulation(population),
        domain.setUser(user)
        domain.getMapper().save(domain)

        buildsTownDomain = models.TownBuilds.Factory.TownBuilds_Factory.getDomainFromData(
            models.TownBuilds.Mapper.TownBuilds_Mapper.getDefaultData()
        )
        buildsTownDomain.setTown(domain)
        buildsTownDomain.getMapper().save(buildsTownDomain)

        serviceTownBonus = Service_TownBonus()
        serviceTownBonusDomain = serviceTownBonus.onCreateTown(domain)
        serviceTownBonus.recalculate(serviceTownBonusDomain)

        serviceTownResources = Service_TownResources()
        serviceTownResourcesDomain = serviceTownResources.onCreateTown(domain)
        serviceTownResources.recalculate(serviceTownResourcesDomain)

        return domain
