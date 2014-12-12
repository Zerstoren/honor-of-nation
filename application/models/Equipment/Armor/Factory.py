import models.Abstract.Factory

from collection.EquipmentArmorCollection import Equipment_Armor_Collection

from . import Domain
from . import Mapper


class Equipment_Armor_Factory_Main(models.Abstract.Factory.Abstract_Factory):
    def get(self, _id):
        result = Mapper.Equipment_Armor_Mapper.getById(_id)
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



Equipment_Armor_Factory = Equipment_Armor_Factory_Main()
