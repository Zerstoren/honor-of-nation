from .Abstract import AbstractService
from models.Army.Domain import Army_Domain
from models.Army.Factory import Army_Factory

import system.log


class Service_Army(AbstractService.Service_Abstract):
    def create(self, unit, town, count, user=None):
        domain = Army_Domain()
        domain.setUnit(unit)
        domain.setUser(town.getUser())
        domain.setCount(count)
        domain.setCommander(None)
        domain.setMap(town.getMap())

        domain.getMapper().save(domain)
        return domain

    def get(self, _id, user=None):
        return Army_Factory.get(_id)

    def load(self, armyUser, position, user=None):
        return Army_Factory.getByPosition(armyUser, position)

    def decorate(self, *args):
        """
        required for IDE static analyzer
        :rtype: Service_Army
        """
        return super().decorate(*args)
