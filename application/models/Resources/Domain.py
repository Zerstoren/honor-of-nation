import models.Abstract.Domain
from .Mapper import Resources_Mapper
from . import Common

import models.User.Factory
import models.User.Domain

import exceptions.resources


class Resources_Domain(models.Abstract.Domain.Abstract_Domain):
    def dropResources(self, data):
        if data[Common.RUBINS] > self.getRubins() or data[Common.WOOD] > self.getWood() or \
           data[Common.STONE] > self.getStone() or data[Common.STEEL] > self.getSteel() or \
           data[Common.EAT] > self.getEat():
            raise exceptions.resources.NotEnoughResources('Not enough resources')

        self.setRubins(self.getRubins() - data[Common.RUBINS])
        self.setRubins(self.getWood() - data[Common.WOOD])
        self.setRubins(self.getStone() - data[Common.STONE])
        self.setRubins(self.getSteel() - data[Common.STEEL])
        self.setRubins(self.getEat() - data[Common.EAT])


    def upResources(self, data):
        self.setRubins(self.getRubins() + data[Common.RUBINS])
        self.setRubins(self.getWood() + data[Common.WOOD])
        self.setRubins(self.getStone() + data[Common.STONE])
        self.setRubins(self.getSteel() + data[Common.STEEL])
        self.setRubins(self.getEat() + data[Common.EAT])

    def getUser(self):
        return models.User.Factory.User_Factory.getDomainById(
            self._getFunc('user')()
        )

    def setUser(self, user):
        if isinstance(user, models.User.Domain.User_Domain):
            self._setFunc('user')(user.getId())
        else:
            self._setFunc('user')(user)

    def getMapper(self):
        return Resources_Mapper

    def toDict(self):
        result = super().toDict()

        del result['user']
        del result['_id']

        return result