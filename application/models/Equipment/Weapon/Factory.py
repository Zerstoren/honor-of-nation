import models.Abstract.Factory

from collection.EquipmentWeaponCollection import Equipment_Weapon_Collection

from . import Domain
from . import Mapper


class Equipment_Weapon_Factory_Main(models.Abstract.Factory.Abstract_Factory):
    def get(self, _id, force=False):
        result = Mapper.Equipment_Weapon_Mapper.getById(_id, force)
        domain = Domain.Equipment_Weapon_Domain()
        domain.setOptions(result)

        return domain

    def load(self, user):
        result = Mapper.Equipment_Weapon_Mapper.getByUser(user)
        collection = Equipment_Weapon_Collection()

        for item in result:
            domain = Domain.Equipment_Weapon_Domain()
            domain.setOptions(item)
            collection.append(domain)

        return collection

    def getDomainFromData(self, data, price=None):
        domain = Domain.Equipment_Weapon_Domain()

        if '_id' in data:
            domain.setId(data['_id'])

        domain.setType(data['type'])
        domain.setDamage(data['damage'])
        domain.setSpeed(data['speed'])
        domain.setCriticalChance(data['critical_chance'])
        domain.setCriticalDamage(data['critical_damage'])

        if price:
            domain.setLevel(price['level'])
            domain.setTime(price['time'])

            domain.setRubins(price['rubins'])
            domain.setWood(price['wood'])
            domain.setSteel(price['steel'])
            domain.setEat(price['eat'])

        return domain

Equipment_Weapon_Factory = Equipment_Weapon_Factory_Main()
