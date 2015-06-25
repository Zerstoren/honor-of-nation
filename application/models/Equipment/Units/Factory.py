import models.Abstract.Factory

from collection.EquipmentUnitsCollection import Equipment_Units_Collection

from models.Equipment.Units.Domain import Equipment_Units_Domain

import models.Equipment.Units.Common as Common

from . import Domain
from . import Mapper


class Equipment_Units_Factory_Main(models.Abstract.Factory.Abstract_Factory):
    def get(self, _id, force=False):
        result = Mapper.Equipment_Units_Mapper.getById(_id, force=force)
        domain = Domain.Equipment_Units_Domain()
        domain.setOptions(result)

        return domain

    def load(self, user):
        result = Mapper.Equipment_Units_Mapper.getByUser(user)
        collection = Equipment_Units_Collection()

        for item in result:
            domain = Domain.Equipment_Units_Domain()
            domain.setOptions(item)
            collection.append(domain)

        return collection

    def getDomainFromData(self, data, price=None):
        domain = Equipment_Units_Domain()

        if '_id' in data and data['_id']:
            domain.setId(data['_id'])
        else:
            domain._loaded = True

        domain.setType(data['type'])
        domain.setHealth(data['health'])
        domain.setAgility(data['agility'])
        domain.setAbsorption(data['absorption'])
        domain.setStamina(data['stamina'])
        domain.setStrength(data['strength'])

        domain.setArmor(data['armor'])
        domain.setWeapon(data['weapon'])
        domain.setWeaponSecond(data['weapon_second'])

        if domain.getType() == Common.TYPE_SOLIDER:
            data['troop_size'] = 0

        domain.setTroopSize(data['troop_size'])

        if price:
            domain.setTime(price['time'])

            domain.setRubins(price['rubins'])
            domain.setWood(price['wood'])
            domain.setSteel(price['steel'])
            domain.setEat(price['eat'])

        return domain


Equipment_Units_Factory = Equipment_Units_Factory_Main()
