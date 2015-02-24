from tests.package import abstract

import models.Town.Domain
import helpers.MapCoordinate
import models.TownBuilds.Factory
import models.TownBuilds.Mapper

from service.Town import Service_Town
from service.TownBonus import Service_TownBonus
from service.TownResources import Service_TownResources

class Town(abstract.AbstractDeclaration):
    TOWN_TYPE_VILLAGE = 0
    TOWN_TYPE_CITY = 1
    TOWN_TYPE_CASTLE = 2

    TOWN_BUILD_FIELD = 'field'                # Поля
    TOWN_BUILD_FARM = 'farm'                  # Фермы
    TOWN_BUILD_MILL = 'mill'                  # Мельницы
    TOWN_BUILD_MINE = 'mine'                  # Шахты
    TOWN_BUILD_ROAD = 'road'                  # Дороги
    TOWN_BUILD_STORAGE = 'storage'            # Хранилища
    TOWN_BUILD_V_COUNCIL = 'v_council'        # Сель. совет
    TOWN_BUILD_T_COUNCIL = 't_council'        # Гор. совет
    TOWN_BUILD_HEADQUARTERS = 'headquarters'  # Штаб
    TOWN_BUILD_GUILDHALL = 'guildhall'        # Ратуша
    TOWN_BUILD_HUT = 'hut'                    # Хибара
    TOWN_BUILD_HOUSE = 'house'                # Дом
    TOWN_BUILD_SMITHY = 'smithy'              # Кузня
    TOWN_BUILD_CASERN = 'casern'              # Казарма
    TOWN_BUILD_BARRACK = 'barrack'            # Бараки
    TOWN_BUILD_PRISON = 'prison'              # Тюрьма
    TOWN_BUILD_HIGH_WALL = 'high_wall'        # Высокие стены
    TOWN_BUILD_WALL = 'wall'                  # Стены

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

    def addTownBuild(self, town, name, level):
        builds = town.getBuilds()
        builds.set(name, level)
        builds.getMapper().save(builds)

        Service_Town().updateBonusAndResources(town)
