import models.Abstract.Domain
from .Mapper import UserState_Mapper


class UserState_Domain(models.Abstract.Domain.Abstract_Domain):
    def getMapper(self):
        """
        required method, for IDE static analyzer
        """
        return UserState_Mapper
