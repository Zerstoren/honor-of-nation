from . import Abstract
import models.MapResources.Domain

class MapResources_Collection(Abstract.AbstractCollection):
    domain = models.MapResources.Domain.MapResources_Domain
