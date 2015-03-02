import models.Abstract.Domain
from .Mapper import Army_Mapper

from models.User.Domain import User_Domain
import models.User.Factory

from models.Equipment.Units.Domain import Equipment_Units_Domain
import models.Equipment.Units.Factory

import time
import config

import models.Map.Factory

class Army_Domain(models.Abstract.Domain.Abstract_Domain):
    def setUser(self, user):
        if isinstance(user, User_Domain):
            self.set('user', user.getId())
        else:
            self.set('user', user)

    def getUser(self):
        userId = self.get('user')
        return models.User.Factory.User_Factory.getDomainById(userId)

    def setUnit(self, unit):
        if isinstance(unit, Equipment_Units_Domain):
            self.set('unit', unit.getId())
        else:
            self.set('unit', unit)

    def getUnit(self):
        unitId = self.get('unit')
        return models.Equipment.Units.Factory.Equipment_Units_Factory.get(unitId, True)

    def setCommander(self, commander):
        if isinstance(commander, Army_Domain):
            self.set('commander', commander.getId())
        else:
            self.set('commander', commander)

    def getPower(self):
        power = self.get('power')
        lastUpdate = self.getLastPowerUpdate()
        currentTime = int(time.time())

        if lastUpdate != currentTime:
            restoredPower = (currentTime - lastUpdate) / int(config.get('army.infantry.power_restore'))

            if power + restoredPower <= 100:
                self.set('power', power + restoredPower)
            elif power + restoredPower >= 100 and self.getInBuild() == False:
                self.set('power', 100)
            elif power + restoredPower <= 150 and self.getInBuild():
                self.set('power', power + restoredPower)
            elif power + restoredPower >= 150 and self.getInBuild():
                self.set('power', power + restoredPower)

            self.setLastPowerUpdate(currentTime)
            self.getMapper().save(self)

        return self.get('power')

    def getCommander(self):
        from . import Factory
        commanderId = self.get('commander')

        if commanderId is None:
            return None

        return Factory.Army_Factory.get(commanderId)

    def setSuite(self, suite):
        if isinstance(suite, Army_Domain):
            self.set('suite', suite.getId())
        else:
            self.set('suite', suite)

    def getSuite(self):
        from . import Factory
        suiteId = self.get('suite')

        if suiteId is None:
            return None

        return Factory.Army_Factory.get(suiteId)

    def setMap(self, location):
        self.set('location', location.getPosition().getPosId())

    def getMap(self):
        return models.Map.Factory.Map_Factory.getDomainById(self.get('location'))

    def setMovePath(self, value):
        if value is None:
            value = []

        self.set('move_path', value)

    def getMapper(self):
        """
        required method, for IDE static analyzer
        """
        return Army_Mapper
