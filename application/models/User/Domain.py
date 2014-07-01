import models.Abstract.Domain
from .Mapper import User_Mapper
import copy


class User_Domain(models.Abstract.Domain.Abstract_Domain):
    _transfer = None

    def getMapper(self):
        return User_Mapper

    def passwordEqual(self, password):
        return self.getPassword() == password

    def _setTransfer(self, transfer):
        self._transfer = transfer

    def hasTransfer(self):
        return self._transfer is not None

    def getTransfer(self):
        return self._transfer

    def toDict(self):
        result = copy.deepcopy(self._domain_data)
        if '_id' in result:
            result['_id'] = str(result['_id'])

        return result
