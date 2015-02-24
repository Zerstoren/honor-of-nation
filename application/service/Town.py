import service.Abstract.AbstractService

import service.TownResources
import service.TownBonus

import models.TownBuilds.Factory
import models.TownBuilds.Mapper

import models.Town.Factory
import models.Town.Common

import config


class Service_Town(service.Abstract.AbstractService.Service_Abstract):
    def getById(self, townId):
        return models.Town.Factory.Town_Factory.getDomainById(townId)

    def loadByPosition(self, mapCoordinate):
        """
        :type mapCoordinate: helpers.MapCoordinate.MapCoordinate
        """
        return models.Town.Factory.Town_Factory.getByPosition(mapCoordinate)

    def save(self, townData):
        domain = models.Town.Factory.Town_Factory.getDomainFromData(townData)
        domain.getMapper().save(domain)

        buildsTownDomain = models.TownBuilds.Factory.TownBuilds_Factory.getDomainFromData(
            models.TownBuilds.Mapper.TownBuilds_Mapper.getDefaultData()
        )
        buildsTownDomain.setTown(domain)

        buildsTownDomain.getMapper().save(buildsTownDomain)

        service.TownBonus.Service_TownBonus().onCreateTown(domain)
        service.TownResources.Service_TownResources().onCreateTown(domain)
        self.updateBonusAndResources(domain)

        return domain

    def updateBonusAndResources(self, town):
        townBonus = service.TownBonus.Service_TownBonus()
        townBonus.recalculate(town.getBonus())

        townResource = service.TownResources.Service_TownResources()
        townResource.recalculate(town.getResourcesUp())

    def getUserTownsCollection(self, user):
        return models.Town.Factory.Town_Factory.getByUser(user)

    def getCollectionByTown(self, town):
        return models.Town.Factory.Town_Factory.getCollectionByTown(town)

    def getAllTownsCollection(self):
        return models.Town.Factory.Town_Factory.getAll()

    def upPopulation(self, town):
        base = 0
        max = 0

        if town.getType() == models.Town.Common.VILLAGE:
            base = int(config.get('population.up.village'))
            max =  int(config.get('population.max_base_population.village'))
        elif town.getType() == models.Town.Common.CITY:
            base = int(config.get('population.up.city'))
            max =  int(config.get('population.max_base_population.city'))
        elif town.getType() == models.Town.Common.CASTLE:
            base = int(config.get('population.up.castle'))
            max =  int(config.get('population.max_base_population.castle'))

        townBonus = town.getBonus()
        max += townBonus.getMaxVillagers()

        population = town.getPopulation()
        if population == max:
            return False

        newPopulation = population + base + townBonus.getVillagers()
        if newPopulation >= max:
            newPopulation = max

        town.setPopulation(newPopulation)

        town.getMapper().save(town)
        return True

    def decorate(self, *args):
        """
        :rtype: Service_Town
        """
        return super().decorate(*args)
