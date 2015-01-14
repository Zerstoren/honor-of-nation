import models.Abstract.Factory

from collection.EquipmentUnitsCollection import Equipment_Units_Collection

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



Equipment_Units_Factory = Equipment_Units_Factory_Main()
