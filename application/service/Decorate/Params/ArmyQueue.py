import service.Town
import service.Equipment.Units

from models.ArmyQueue.Factory import ArmyQueue_Factory

"""
Access Layer Level for decorate base service class
"""
class Decorate():
    def add(self, town, unit, count, user=None):
        town = service.Town.Service_Town().getById(town)
        unit = service.Equipment.Units.Service_Equipment_Units().getForce(unit)
        count = int(count)

        return super().add(town, unit, count, user)

    def remove(self, town, queueDomain, user=None):
        town = service.Town.Service_Town().getById(town)
        queueDomain = ArmyQueue_Factory.get(queueDomain)
        return super().remove(town, queueDomain, user)

    def getQueue(self, town, user=None):
        town = service.Town.Service_Town().getById(town)
        return super().getQueue(town, user)
