from .Abstract import AbstractService

from models.TownBuilds.Data import builds
from models.TownBonus.Factory import TownBonus_Factory

class Service_TownBonus(AbstractService.Service_Abstract):
    def get(self, town):
        return TownBonus_Factory.get(town)

    def onCreateTown(self, townDomain):
        from models.TownBonus.Domain import TownBonus_Domain
        domain = TownBonus_Domain()
        domain.setTown(townDomain)
        domain.setEat(0)
        domain.setMinerals(0)
        domain.setTax(0)
        domain.setBuildsSpeed(0)
        domain.setRiot(0)
        domain.setVillagers(0)
        domain.setMaxVillagers(0)
        domain.setArmorySpeed(0)
        domain.setArmoryPrice(0)
        domain.setWeaponSpeed(0)
        domain.setWeaponPrice(0)
        domain.setSolidersSpeed(0)
        domain.setCityDefence(0)
        domain.setCitySteps(0)

        domain.getMapper().save(domain)

        return domain

    def recalculate(self, domain):
        townDomain = domain.getTown()
        townBuilds = townDomain.getBuilds()

        for buildKey in builds:
            buildLevel = townBuilds.get(buildKey)

            if buildLevel == 0:
                continue

            for bonusKey in builds[buildKey]['bonus']:
                bonusUp = domain.get(bonusKey) + (builds[buildKey]['bonus'][bonusKey] * buildLevel)
                domain.set(bonusKey, bonusUp)

        domain.getMapper().save(domain)

    def decorate(self, *args):
        """
        required for IDE static analyzer
        :rtype: Service_TownBonus
        """
        return super().decorate(*args)
