import models.Abstract.Domain
from .Mapper import Example_Mapper


class Example_Domain(models.Abstract.Domain.Abstract_Domain):
    def getMapper(self):
        """
        required method, for IDE static analyzer
        """
        return Example_Mapper
