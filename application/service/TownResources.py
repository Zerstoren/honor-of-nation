from .Abstract import AbstractService
from models.TownResources.Domain import TownResources_Domain

from models.Town import Common as Common_Town
from models.Resources import Common as Common_Resources

import service.MapResources

import config
import helpers.math

class Service_TownResources(AbstractService.Service_Abstract):

    def onCreateTown(self, townDomain):
        domain = TownResources_Domain()
        domain.setTax(0)
        domain.setRubins(0)
        domain.setSteel(0)
        domain.setWood(0)
        domain.setEat(0)
        domain.setStone(0)
        domain.setTown(townDomain)

        domain.getMapper().save(domain)

        return domain

    def recalculate(self, domain):
        townDomain = domain.getTown()
        townBonus = townDomain.getBonus()
        mapResourcesCollection = service.MapResources.Service_MapResources().getResourceByTown(townDomain)
        mapResourcesCollection.extract()

        minerals = self._getMinerals(townBonus, mapResourcesCollection)
        domain.setTax(self._getTaxSize(townDomain, townBonus))
        domain.setEat(self._getEat(townBonus, mapResourcesCollection))
        domain.setWood(self._getWood(townBonus, mapResourcesCollection))
        domain.setRubins(minerals[Common_Resources.RUBINS])
        domain.setStone(minerals[Common_Resources.STONE])
        domain.setSteel(minerals[Common_Resources.STEEL])

        domain.getMapper().save(domain)

    def _getTaxSize(self, town, townBonus):
        population = town.getPopulation()

        baseTax = 0

        if town.getType() == Common_Town.VILLAGE:
            baseTax = int(config.get('tax.village'))
        elif town.getType() == Common_Town.CITY:
            baseTax = int(config.get('tax.city'))

        return population * (baseTax + townBonus.getTax())

    def _getEat(self, townBonus, mapResourcesCollection):
        eatCollection = mapResourcesCollection.filter('type', Common_Resources.EAT)
        output = 0

        for eat in eatCollection:
            output += helpers.math.percent(eat.getBaseOutput(), townBonus.getEat() + 100)

        return output

    def _getWood(self, townBonus, mapResourcesCollection):
        woodCollection = mapResourcesCollection.filter('type', Common_Resources.WOOD)
        output = 0

        for wood in woodCollection:
            output += wood.getBaseOutput()

        return output

    def _getMinerals(self, townBonus, mapResourcesCollection):
        search = [Common_Resources.RUBINS, Common_Resources.STONE, Common_Resources.STEEL]
        mineralBonus = townBonus.getMinerals()

        result = {}

        for mineral in search:
            collection = mapResourcesCollection.filter('type', mineral)
            output = 0

            for mineralResource in collection:
                output += helpers.math.percent(mineralResource.getBaseOutput(), mineralBonus + 100)

            result[mineral] = output

        return result

    def decorate(self, *args):
        """
        required for IDE static analyzer
        :rtype: Service_TownResources
        """
        return super().decorate(*args)
