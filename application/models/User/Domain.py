import models.Abstract.Domain
from .Mapper import User_Mapper

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
        if not self._transfer:
            import system.UserTransfer
            self._transfer = system.UserTransfer.UserTransfer()
            self._transfer.setUser(self)

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
        self.set('position', {
            'x': int(x),
            'y': int(y)
        })

    def toDict(self):
        result = super().toDict()
        del result['password']

        return result
