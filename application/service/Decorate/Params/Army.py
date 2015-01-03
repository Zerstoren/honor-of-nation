import service.Town
import service.Equipment.Units

"""
Access Layer Level for decorate base service class
"""
class Decorate():
    def create(self, unit, town, count, user=None):
        town = service.Town.Service_Town().getById(town)
        unit = service.Equipment.Units.Service_Equipment_Units().getForce(unit)
        count = int(count)

        return super().create(unit, town, count, user)
