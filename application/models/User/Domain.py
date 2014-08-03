import models.Abstract.Domain
from .Mapper import User_Mapper
import copy

import models.Resources.Mapper
import models.Resources.Domain


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

    def getResources(self):
        """
        :type userDomain: models.User.Domain.User_Domain
        """
        domain = models.Resources.Domain.Resources_Domain()

        domain.setOptions(
            models.Resources.Mapper.Resources_Mapper.getByUser(self)
        )

        return domain

    def setPosition(self, x, y):
        self._domain_data['position'] = {
            'x': int(x),
            'y': int(y)
        }

    def toDict(self):
        result = copy.deepcopy(self._domain_data)
        if '_id' in result:
            result['_id'] = str(result['_id'])

        return result
