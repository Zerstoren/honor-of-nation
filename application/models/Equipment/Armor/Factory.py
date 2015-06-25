import models.Abstract.Factory

from collection.EquipmentArmorCollection import Equipment_Armor_Collection

from . import Domain
from . import Mapper


class Equipment_Armor_Factory_Main(models.Abstract.Factory.Abstract_Factory):
    def get(self, _id, force=False):
        result = Mapper.Equipment_Armor_Mapper.getById(_id, force)
        domain = Domain.Equipment_Armor_Domain()
        domain.setOptions(result)

        return domain

    def load(self, user):
        result = Mapper.Equipment_Armor_Mapper.getByUser(user)
        collection = Equipment_Armor_Collection()

        for item in result:
            domain = Domain.Equipment_Armor_Domain()
            domain.setOptions(item)
            collection.append(domain)

        return collection

    def getDomainFromData(self, data):
        domain = Domain.Equipment_Armor_Domain()

        if '_id' in data:
            domain.setId(data['_id'])

        domain.setType(data['type'])
        domain.setHealth(data['health'])
        domain.setAgility(data['agility'])
        domain.setAbsorption(data['absorption'])

        domain.setShield(data['shield'])
        domain.setShieldType(data['shield_type'])
        domain.setShieldDurability(data['shield_durability'])
        domain.setShieldBlocking(data['shield_blocking'])

        return domain

Equipment_Armor_Factory = Equipment_Armor_Factory_Main()
